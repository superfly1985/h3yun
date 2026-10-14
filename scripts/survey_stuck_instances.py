# -*- coding: utf-8 -*-
"""
摸底生产表单"进行中"流程实例分布
用法:
    python scripts/survey_stuck_instances.py                # 全量
    python scripts/survey_stuck_instances.py --limit 200    # 只测前200条
输出: scripts/stuck_instances.json (进行中实例清单, 供批量结束用)
"""
import argparse
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and "=" in s and not s.startswith("#"):
            k, v = s.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

from h3yun import H3YunConfig, H3YunClient  # noqa: E402

FORM_CODE = "D287764b96d54298e814d06b87e5f99a28658ad"
APP_CODE = "D287764D287765"  # 生产应用（控制器 WfFixController 所在）
CONTROLLER = "WfFixController"
OUT_FILE = Path(__file__).parent / "stuck_instances.json"
PAGE = 500


def load_env_conf():
    return H3YunConfig.from_env()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只处理前N条有实例的记录, 0=全量")
    ap.add_argument("--out", default=str(OUT_FILE), help="输出文件")
    ap.add_argument("--finish", type=int, default=0, help="测试: 结束前N个进行中实例")
    args = ap.parse_args()

    client = H3YunClient(load_env_conf())

    # ---- 1. 部署验证: 用一个必然不存在的实例Id查状态 ----
    print("== 1. 部署验证 (QueryInstanceStates) ==")
    r = client.invoke("QueryInstanceStates", {
        "Controller": CONTROLLER,
        "AppCode": APP_CODE,
        "InstanceIds": "00000000-0000-0000-0000-000000000000",
    })
    rd = r.get("ReturnData", {})
    print("   返回:", json.dumps(rd, ensure_ascii=False))
    if rd.get("result") != "success":
        print("!! 部署验证失败，v3 未生效")
        sys.exit(1)

    # ---- 2. 全表拉取记录 (ObjectId + WorkflowInstanceId + 线号 + 产线 + 时间) ----
    print("== 2. 全表分页拉取实例清单 ==")
    records = []
    from_row = 0
    t0 = time.time()
    while True:
        flt = H3YunClient.build_filter(
            from_row_num=from_row, to_row_num=from_row + PAGE,
            return_items=["ObjectId", "WorkflowInstanceId", "F0000014", "F0000001", "CreatedTime", "Status"],
        )
        arr = client.load_biz_objects(FORM_CODE, filter_str=flt)["ReturnData"]["BizObjectArray"]
        if not arr:
            break
        records.extend(arr)
        if len(arr) < PAGE:
            break
        from_row += PAGE
        if from_row % 5000 == 0:
            print(f"   已拉取 {from_row} 条... ({time.time()-t0:.0f}s)")
    print(f"   全表 {len(records)} 条, 耗时 {time.time()-t0:.0f}s")

    with_inst = [it for it in records if it.get("WorkflowInstanceId")]
    print(f"   有流程实例的: {len(with_inst)} 条")
    if args.limit > 0:
        with_inst = with_inst[: args.limit]
        print(f"   (--limit) 只处理前 {len(with_inst)} 条")

    # ---- 3. 分批查实例状态 (每批500, 只读) ----
    print("== 3. 分批查询实例状态 (只读) ==")
    ids = [it["WorkflowInstanceId"] for it in with_inst]
    state_map = {}  # instanceId -> state
    for i in range(0, len(ids), PAGE):
        chunk = ids[i:i + PAGE]
        rd = client.invoke("QueryInstanceStates", {
            "Controller": CONTROLLER,
            "AppCode": APP_CODE,
            "InstanceIds": ",".join(chunk),
        })["ReturnData"]
        # runningIds 是 1/2 状态的; 其余按 skipped 处理(状态值不必逐条知道)
        running_set = set(x for x in (rd.get("runningIds") or "").split(",") if x)
        for iid in chunk:
            state_map[iid] = 1 if iid in running_set else 9  # 9=非进行中(4/5/不存在)
        done = min(i + PAGE, len(ids))
        print(f"   {done}/{len(ids)} ({time.time()-t0:.0f}s)")

    # ---- 4. 汇总进行中实例, 存盘 + 分布统计 ----
    stuck = []
    for it in with_inst:
        if state_map.get(it["WorkflowInstanceId"]) == 1:
            stuck.append({
                "ObjectId": it.get("ObjectId") or "",
                "WorkflowInstanceId": it["WorkflowInstanceId"],
                "F0000014": it.get("F0000014") or "",
                "F0000001": it.get("F0000001") or "",
                "CreatedTime": it.get("CreatedTime") or "",
            })

    print("== 4. 汇总 ==")
    print(f"真正进行中的实例: {len(stuck)} 个")
    by_month = Counter(s["CreatedTime"][:7] for s in stuck)
    print("按月分布:", dict(sorted(by_month.items())))
    by_line = Counter(s["F0000001"] or "(空)" for s in stuck)
    print("按产线(F0000001):", dict(by_line))

    out_path = Path(args.out)
    out_path.write_text(json.dumps(stuck, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"清单已保存: {out_path}")

    # ---- 5. 可选: 小批量测试结束前N个 ----
    if args.finish > 0:
        targets = stuck[: args.finish]
        print(f"== 5. 测试结束前 {len(targets)} 个进行中实例 ==")
        ids = ",".join(t["WorkflowInstanceId"] for t in targets)
        rd = client.invoke("FinishInstanceBatch", {
            "Controller": CONTROLLER,
            "AppCode": APP_CODE,
            "InstanceIds": ids,
        })["ReturnData"]
        print("   结果:", json.dumps(rd, ensure_ascii=False))


if __name__ == "__main__":
    main()
