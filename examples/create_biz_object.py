# -*- coding: utf-8 -*-
"""
示例：创建单条业务数据

Usage:
    python examples/create_biz_object.py --schema SchemaCode --data '{"Name":"test"}'
    python examples/create_biz_object.py --schema SchemaCode --file data.json

Example:
    python examples/create_biz_object.py --schema D000001test --data '{"Name":"张三","Age":25}'
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

    parser = argparse.ArgumentParser(description="创建单条业务数据")
    parser.add_argument("--schema", required=True, help="表单编码 (SchemaCode)")
    parser.add_argument("--data", help="业务数据JSON字符串")
    parser.add_argument("--file", help="业务数据JSON文件路径")
    parser.add_argument("--draft", action="store_true", help="保存为草稿（不提交）")
    args = parser.parse_args()

    if not args.data and not args.file:
        parser.error("请提供 --data 或 --file 参数")

    # 读取业务数据
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            biz_data = json.load(f)
    else:
        biz_data = json.loads(args.data)

    config = H3YunConfig.from_env()
    client = H3YunClient(config)

    try:
        result = client.create_biz_object(
            args.schema,
            biz_data,
            is_submit=not args.draft
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
