import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from Web_Service.氚云.src.h3yun_config import H3YunConfig
from Web_Service.氚云.src.h3yun_client import H3YunClient


def apply_env():
    p = Path(__file__).resolve().parents[1] / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and "=" in s and not s.startswith("#"):
                k, v = s.split("=", 1)
                os.environ[k.strip()] = v.strip()


def main():
    apply_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--from", dest="from_row", type=int, default=0)
    ap.add_argument("--to", dest="to_row", type=int, default=50)
    ap.add_argument("--require-count", dest="require_count", type=str, default="true")
    ap.add_argument("--return-items", dest="return_items", default="[\"ObjectId\",\"Name\",\"IP\",\"pic\"]")
    ap.add_argument("--sort-by", dest="sort_by", default="[]")
    ap.add_argument("--field", dest="field", default=None)
    ap.add_argument("--value", dest="value", default=None)
    args = ap.parse_args()
    cfg = H3YunConfig.from_env()
    client = H3YunClient(cfg)
    matcher = {"Type": "And", "Matchers": []}
    if args.field and args.value:
        matcher = {"Type": "And", "Matchers": [{"Type": "Equal", "Left": args.field, "Right": args.value}]}
    fobj = {
        "FromRowNum": args.from_row,
        "RequireCount": args.require_count.lower() == "true",
        "ReturnItems": json.loads(args.return_items),
        "SortByCollection": json.loads(args.sort_by),
        "ToRowNum": args.to_row,
        "Matcher": matcher,
    }
    params = {"Filter": json.dumps(fobj, ensure_ascii=False, separators=(",", ":"))}
    res = client.load_biz_objects(args.schema, params)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()

