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
    ap.add_argument("--value", required=True)
    args = ap.parse_args()
    cfg = H3YunConfig.from_env()
    client = H3YunClient(cfg)
    biz = {args.field: args.value}
    res = client.update_biz_object(args.schema, args.id, biz)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()

