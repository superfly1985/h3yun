# -*- coding: utf-8 -*-
"""
示例：上传附件

Usage:
    python examples/upload_attachment.py --schema SchemaCode --id BizObjectId --field FilePropertyName --file /path/to/file

Example:
    python examples/upload_attachment.py --schema D000001test --id xxx --field pic --file image.png
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

    parser = argparse.ArgumentParser(description="上传附件")
    parser.add_argument("--schema", required=True, help="表单编码 (SchemaCode)")
    parser.add_argument("--id", required=True, help="业务对象ID (BizObjectId)")
    parser.add_argument("--field", required=True, help="文件属性名 (FilePropertyName)")
    parser.add_argument("--file", required=True, help="本地文件路径")
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: 文件不存在: {args.file}")
        sys.exit(1)

    config = H3YunConfig.from_env()
    client = H3YunClient(config)

    try:
        result = client.upload_attachment(
            args.schema,
            args.id,
            args.field,
            args.file
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
