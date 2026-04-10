# -*- coding: utf-8 -*-
"""
示例：更新业务数据

Usage:
    python examples/update_biz_object.py --schema SchemaCode --id BizObjectId --data '{"Name":"new name"}'
    python examples/update_biz_object.py --schema SchemaCode --id BizObjectId --file update.json

Example:
    python examples/update_biz_object.py --schema D000001test --id xxx --data '{"Status":"已完成"}'
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

    parser = argparse.ArgumentParser(description="更新业务数据")
    parser.add_argument("--schema", required=True, help="表单编码 (SchemaCode)")
    parser.add_argument("--id", required=True, help="业务对象ID (BizObjectId)")
    parser.add_argument("--data", help="更新数据JSON字符串")
    parser.add_argument("--file", help="更新数据JSON文件路径")
    args = parser.parse_args()

    if not args.data and not args.file:
        parser.error("请提供 --data 或 --file 参数")

    # 读取更新数据
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            biz_data = json.load(f)
    else:
        biz_data = json.loads(args.data)

    config = H3YunConfig.from_env()
    client = H3YunClient(config)

    try:
        result = client.update_biz_object(args.schema, args.id, biz_data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
