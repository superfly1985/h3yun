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
    ap.add_argument("--id", required=True)
    ap.add_argument("--field", required=True)
    ap.add_argument("--out", required=False)
    args = ap.parse_args()
    cfg = H3YunConfig.from_env()
    client = H3YunClient(cfg)
    res = client.load_biz_object(args.schema, args.id)
    bo = (res.get("ReturnData") or {}).get("BizObject") or {}
    arr = bo.get(args.field) or []
    if isinstance(arr, str):
        arr = [arr]
    out_dir = args.out or str(Path(__file__).resolve().parents[1] / "download" / args.field)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    items = []
    for aid in arr:
        items.append({"attachmentId": aid, "saved": client.download_attachment(aid, out_dir)})
    print(json.dumps({"ok": True, "count": len(items), "out": out_dir, "items": items}, ensure_ascii=False))


if __name__ == "__main__":
    main()

