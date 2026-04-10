# -*- coding: utf-8 -*-
"""
示例：下载附件

Usage:
    python examples/download_attachment.py --id AttachmentId [--out /path/to/output]

Example:
    python examples/download_attachment.py --id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    python examples/download_attachment.py --id xxx --out ./downloads
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.h3yun import H3YunConfig, H3YunClient


def apply_env():
    p = Path(__file__).resolve().parent.parent / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and "=" in s and not s.startswith("#"):
                k, v = s.split("=", 1)
                os.environ[k.strip()] = v.strip()


def main():
    apply_env()

    parser = argparse.ArgumentParser(description="下载附件")
    parser.add_argument("--id", required=True, help="附件ID (AttachmentId)")
    parser.add_argument("--out", help="输出目录，默认 ./download")
    parser.add_argument("--filename", help="指定文件名")
    args = parser.parse_args()

    config = H3YunConfig.from_env()
    client = H3YunClient(config)

    try:
        result = client.download_attachment(
            args.id,
            out_dir=args.out,
            filename=args.filename
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
