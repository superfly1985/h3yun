# -*- coding: utf-8 -*-
"""
全量批量结束生产表单"进行中"的流程实例 (v2: 只结束进行中的, 小批+失败自动拆半重试+断点续跑)
用法:
    python scripts/finish_all_stuck.py            # 执行
    python scripts/finish_all_stuck.py --verify   # 只复查剩余进行中数量
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and "=" in s and not s.startswith("#"):
            k, v = s.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from h3yun import H3YunConfig, H3YunClient, H3YunAPIError  # noqa: E402

FORM_CODE = "D287764b96d54298e814d06b87e5f99a28658ad"
APP_CODE = "D287764D287765"
CONTROLLER = "WfFixController"
PAGE = 500
RUNNING_FILE = Path(__file__).parent / "running_ids.json"
CKPT = Path(__file__).parent / "finish_checkpoint.json"
LOG = Path(__file__).parent / "finish_log.jsonl"


def load_all_ids(client):
    out = []
    from_row = 0
    t0 = time.time()
    while True:
        flt = H3YunClient.build_filter(
            from_row_num=from_row, to_row_num=from_row + PAGE,
            return_items=["ObjectId", "WorkflowInstanceId", "F0000001", "CreatedTime"],
        )
        arr = client.load_biz_objects(FORM_CODE, filter_str=flt)["ReturnData"]["BizObjectArray"]
        if not arr:
            break
        for it in arr:
            if it.get("WorkflowInstanceId"):
                out.append(it["WorkflowInstanceId"])
        if len(arr) < PAGE:
            break
        from_row += PAGE
    print(f"拉取完成: {len(out)} 个流程实例, 耗时 {time.time()-t0:.0f}s")
    return out


def query_running(client, ids):
    running = []
    t0 = time.time()
    for i in range(0, len(ids), PAGE):
        chunk = ids[i:i + PAGE]
        rd = client.invoke("QueryInstanceStates", {
            "Controller": CONTROLLER, "AppCode": APP_CODE,
            "InstanceIds": ",".join(chunk),
        })["ReturnData"]
        running.extend(x for x in (rd.get("runningIds") or "").split(",") if x)
        if (i // PAGE) % 10 == 0:
            print(f"  状态查询 {i+len(chunk)}/{len(ids)} ({time.time()-t0:.0f}s)")
    return running


def finish_chunk(client, ids, log_prefix=""):
    """结束一批, 失败自动对半拆分重试; 返回 (finished, skipped, errors)"""
    if not ids:
        return 0, 0, 0
    try:
        rd = client.invoke("FinishInstanceBatch", {
            "Controller": CONTROLLER, "AppCode": APP_CODE,
            "InstanceIds": ",".join(ids),
        })["ReturnData"]
        with LOG.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps({"ids": len(ids), "rd": rd}, ensure_ascii=False) + "\n")
        return (int(rd.get("finished", 0)), int(rd.get("skipped", 0)),
                int(rd.get("error", 0)) + int(rd.get("notfound", 0)))
    except H3YunAPIError as e:
        if len(ids) == 1:
            with LOG.open("a", encoding="utf-8") as fp:
                fp.write(json.dumps({"ids": 1, "id": ids[0], "failed": str(e)[:200]},
                                    ensure_ascii=False) + "\n")
            print(f"  {log_prefix}单条失败(跳过): {ids[0][:8]}... {str(e)[:80]}")
            return 0, 0, 1
        mid = len(ids) // 2
        print(f"  {log_prefix}批次{len(ids)}出错, 拆半重试 {mid}/{len(ids)-mid}: {str(e)[:60]}")
        time.sleep(1)
        f1, s1, e1 = finish_chunk(client, ids[:mid], log_prefix + "  ")
        f2, s2, e2 = finish_chunk(client, ids[mid:], log_prefix + "  ")
        return f1 + f2, s1 + s2, e1 + e2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk-size", type=int, default=50)
    ap.add_argument("--verify", action="store_true", help="只复查剩余进行中数量")
    args = ap.parse_args()

    client = H3YunClient(H3YunConfig.from_env())

    if args.verify:
        all_ids = load_all_ids(client)
        running = query_running(client, all_ids)
        print(f"复查: 剩余进行中实例 {len(running)} 个")
        sys.exit(0)

    # 1. 取进行中清单 (有缓存则复用)
    if RUNNING_FILE.exists():
        running = json.loads(RUNNING_FILE.read_text())
        print(f"复用缓存清单: {len(running)} 个进行中实例 ({RUNNING_FILE})")
    else:
        all_ids = load_all_ids(client)
        print("查询进行中实例...")
        running = query_running(client, all_ids)
        RUNNING_FILE.write_text(json.dumps(running), encoding="utf-8")
        print(f"进行中: {len(running)} 个, 清单已缓存")

    # 2. 分批结束 (断点续跑)
    total_chunks = (len(running) + args.chunk_size - 1) // args.chunk_size
    start_chunk = 0
    if CKPT.exists():
        start_chunk = json.loads(CKPT.read_text())["done_chunks"]
        print(f"从断点继续: 第 {start_chunk+1}/{total_chunks} 批")

    t0 = time.time()
    ok = skip = err = 0
    for ci in range(start_chunk, total_chunks):
        chunk = running[ci * args.chunk_size:(ci + 1) * args.chunk_size]
        f, s, e = finish_chunk(client, chunk, log_prefix=f"[批{ci+1}] ")
        ok += f; skip += s; err += e
        CKPT.write_text(json.dumps({"done_chunks": ci + 1}), encoding="utf-8")
        print(f"批 {ci+1}/{total_chunks} ({len(chunk)}个): finished={f} skipped={s} err={e} "
              f"| 累计结束={ok} ({time.time()-t0:.0f}s)", flush=True)

    print(f"\n执行完成: 结束 {ok} 个, 跳过 {skip} 个, 失败 {err} 个")
    print("建议执行 --verify 复查")


if __name__ == "__main__":
    main()
