import argparse
import json
import os
from pathlib import Path

from .h3yun_config import H3YunConfig
from .h3yun_client import H3YunClient


def build_client() -> H3YunClient:
    cfg = H3YunConfig.from_env()
    return H3YunClient(cfg)


def _apply_env_file(path: str) -> None:
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if "=" in s:
            k, v = s.split("=", 1)
            os.environ[k.strip()] = v.strip()

def main():
    p = argparse.ArgumentParser(prog="h3yun", description="H3Yun form read/write")
    p.add_argument("--env-file", dest="env_file", default=None)
    p.add_argument("--timeout", dest="timeout", type=int, default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("read")
    pr.add_argument("--form", dest="form", default=None)
    pr.add_argument("--query", dest="query", default=None, help="JSON query object")
    pr.add_argument("--action", dest="action", default=None)
    pr.add_argument("--params", dest="params", default=None, help="JSON params object")

    pc = sub.add_parser("create")
    pc.add_argument("--form", dest="form", default=None)
    pc.add_argument("--data", dest="data", required=True, help="JSON data object")
    pc.add_argument("--action", dest="action", default=None)
    pc.add_argument("--params", dest="params", default=None, help="JSON params object")

    pu = sub.add_parser("update")
    pu.add_argument("--form", dest="form", default=None)
    pu.add_argument("--id", dest="rid", required=True)
    pu.add_argument("--data", dest="data", required=True, help="JSON data object")
    pu.add_argument("--action", dest="action", default=None)
    pu.add_argument("--params", dest="params", default=None, help="JSON params object")

    po = sub.add_parser("load-one")
    po.add_argument("--schema", dest="schema", required=True)
    po.add_argument("--id", dest="biz_id", required=True)

    pm = sub.add_parser("load-many")
    pm.add_argument("--schema", dest="schema", required=True)
    pm.add_argument("--params", dest="params", default=None, help="JSON params object")
    pm.add_argument("--from", dest="from_row", type=int, default=0)
    pm.add_argument("--to", dest="to_row", type=int, default=500)
    pm.add_argument("--require-count", dest="require_count", type=str, default="false")
    pm.add_argument("--return-items", dest="return_items", default="[]", help="JSON array string")
    pm.add_argument("--sort-by", dest="sort_by", default="[]", help="JSON array string")
    pm.add_argument("--matcher", dest="matcher", default=None, help="JSON matcher object string")
    pm.add_argument("--matcher-file", dest="matcher_file", default=None, help="JSON matcher file path")

    pc1 = sub.add_parser("create-one")
    pc1.add_argument("--schema", dest="schema", required=True)
    pc1.add_argument("--biz", dest="biz", required=True, help="JSON string or object for BizObject")
    pc1.add_argument("--submit", dest="submit", default="true")

    pcm = sub.add_parser("create-many")
    pcm.add_argument("--schema", dest="schema", required=True)
    pcm.add_argument("--biz-array", dest="biz_array", required=True, help="JSON array string or list of objects")
    pcm.add_argument("--submit", dest="submit", default="true")

    pe = sub.add_parser("export-csv")
    pe.add_argument("--schema", dest="schema", required=True)
    pe.add_argument("--out", dest="out", required=True)
    pe.add_argument("--from", dest="from_row", type=int, default=0)
    pe.add_argument("--to", dest="to_row", type=int, default=500)
    pe.add_argument("--require-count", dest="require_count", type=str, default="false")
    pe.add_argument("--return-items", dest="return_items", default="[]")
    pe.add_argument("--sort-by", dest="sort_by", default="[]")
    pe.add_argument("--matcher", dest="matcher", default=None)
    pe.add_argument("--matcher-file", dest="matcher_file", default=None)
    pe.add_argument("--columns", dest="columns", default=None, help="comma separated column names")

    puo = sub.add_parser("update-one")
    puo.add_argument("--schema", dest="schema", required=True)
    puo.add_argument("--id", dest="biz_id", required=True)
    puo.add_argument("--biz", dest="biz", required=False, help="JSON string or object for BizObject")
    puo.add_argument("--biz-file", dest="biz_file", required=False, help="JSON file path for BizObject")

    prm = sub.add_parser("remove-one")
    prm.add_argument("--schema", dest="schema", required=True)
    prm.add_argument("--id", dest="biz_id", required=True)

    args = p.parse_args()
    if args.env_file:
        _apply_env_file(args.env_file)
    else:
        from pathlib import Path as _P
        _cands = [
            _P('.env'),
            _P('Web_Service/氚云/.env'),
            _P('Web_Service/氚云/test/h3yun.env'),
        ]
        for _p in _cands:
            if _p.exists():
                _apply_env_file(str(_p))
                break
    if args.timeout is not None:
        os.environ["H3YUN_TIMEOUT"] = str(args.timeout)
    client = build_client()

    if args.cmd == "load-one":
        res = client.load_biz_object(args.schema, args.biz_id)
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "load-many":
        if args.params:
            params = json.loads(args.params)
        else:
            if args.matcher_file:
                matcher = json.loads(Path(args.matcher_file).read_text(encoding="utf-8"))
            else:
                matcher = json.loads(args.matcher) if args.matcher else {"Type": "And", "Matchers": []}
            filter_obj = {
                "FromRowNum": args.from_row,
                "RequireCount": args.require_count.lower() == "true",
                "ReturnItems": json.loads(args.return_items),
                "SortByCollection": json.loads(args.sort_by),
                "ToRowNum": args.to_row,
                "Matcher": matcher,
            }
            filter_str = json.dumps(filter_obj, ensure_ascii=False, separators=(",", ":"))
            params = {"Filter": filter_str}
        res = client.load_biz_objects(args.schema, params)
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "create-one":
        biz = json.loads(args.biz) if (args.biz.strip().startswith("{") and args.biz.strip().endswith("}")) else args.biz
        res = client.create_biz_object(args.schema, biz, (args.submit.lower() == "true"))
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "create-many":
        ba = args.biz_array
        if ba.strip().startswith("[") and ba.strip().endswith("]"):
            biz_arr = json.loads(ba)
        else:
            p = Path(ba)
            if p.exists():
                biz_arr = json.loads(p.read_text(encoding="utf-8"))
            else:
                raise SystemExit("--biz-array must be a JSON array string or a JSON file path")
        res = client.create_biz_objects(args.schema, biz_arr, (args.submit.lower() == "true"))
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "update-one":
        if args.biz_file:
            biz = json.loads(Path(args.biz_file).read_text(encoding="utf-8"))
        else:
            if not args.biz:
                raise SystemExit("--biz or --biz-file is required")
            biz = json.loads(args.biz) if (args.biz.strip().startswith("{") and args.biz.strip().endswith("}")) else args.biz
        res = client.update_biz_object(args.schema, args.biz_id, biz)
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "remove-one":
        res = client.remove_biz_object(args.schema, args.biz_id)
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "read":
        if args.params:
            params = json.loads(args.params)
        else:
            cfg = H3YunConfig.from_env()
            q = json.loads(args.query) if args.query else None
            params = {cfg.class_key: args.form or cfg.form_name, "Query": q or {}}
        res = client.invoke(args.action or H3YunConfig.from_env().read_action, params)
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "export-csv":
        if args.matcher_file:
            matcher = json.loads(Path(args.matcher_file).read_text(encoding="utf-8"))
        else:
            matcher = json.loads(args.matcher) if args.matcher else {"Type": "And", "Matchers": []}
        filter_obj = {
            "FromRowNum": args.from_row,
            "RequireCount": args.require_count.lower() == "true",
            "ReturnItems": json.loads(args.return_items),
            "SortByCollection": json.loads(args.sort_by),
            "ToRowNum": args.to_row,
            "Matcher": matcher,
        }
        filter_str = json.dumps(filter_obj, ensure_ascii=False, separators=(",", ":"))
        res = client.load_biz_objects(args.schema, {"Filter": filter_str})
        arr = (res.get("ReturnData") or {}).get("BizObjectArray") or []
        cols = []
        if args.columns:
            cols = [c.strip() for c in args.columns.split(",") if c.strip()]
        else:
            keys = set()
            for o in arr:
                if isinstance(o, dict):
                    keys.update(o.keys())
            pref = ["ObjectId","Name","CreatedBy","OwnerDeptId","oldksk","newksk","IP","date"]
            cols = pref + [k for k in sorted(keys) if k not in pref]
        Path(Path(args.out).parent).mkdir(parents=True, exist_ok=True)
        import csv
        with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for o in arr:
                row = []
                for c in cols:
                    v = o.get(c) if isinstance(o, dict) else None
                    if isinstance(v, (dict, list)):
                        row.append(json.dumps(v, ensure_ascii=False))
                        
                    else:
                        row.append(v if v is not None else "")
                w.writerow(row)
        print(json.dumps({"ok": True, "count": len(arr), "out": args.out}, ensure_ascii=False))
    elif args.cmd == "create":
        data = json.loads(args.data)
        if args.params:
            params = json.loads(args.params)
        else:
            cfg = H3YunConfig.from_env()
            params = {cfg.class_key: args.form or cfg.form_name, "Data": data}
        res = client.invoke(args.action or H3YunConfig.from_env().write_action, params)
        print(json.dumps(res, ensure_ascii=False))
    elif args.cmd == "update":
        data = json.loads(args.data)
        if args.params:
            params = json.loads(args.params)
        else:
            cfg = H3YunConfig.from_env()
            params = {cfg.class_key: args.form or cfg.form_name, "Id": args.rid, "Data": data}
        res = client.invoke(args.action or H3YunConfig.from_env().update_action, params)
        print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
