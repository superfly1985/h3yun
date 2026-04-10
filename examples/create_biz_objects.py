# -*- coding: utf-8 -*-
"""
示例：批量创建业务数据

Usage:
    python examples/create_biz_objects.py --schema SchemaCode --file data.json

Example:
    python examples/create_biz_objects.py --schema D000001test --file batch_data.json
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

    parser = argparse.ArgumentParser(description="批量创建业务数据")
    parser.add_argument("--schema", required=True, help="表单编码 (SchemaCode)")
    parser.add_argument("--file", required=True, help="业务数据JSON文件路径（数组格式）")
    parser.add_argument("--draft", action="store_true", help="保存为草稿（不提交）")
    parser.add_argument("--batch-size", type=int, default=100, help="每批处理数量，默认100")
    args = parser.parse_args()

    # 读取业务数据数组
    with open(args.file, "r", encoding="utf-8") as f:
        biz_objects = json.load(f)

    if not isinstance(biz_objects, list):
        print("Error: 数据文件必须是JSON数组格式")
        sys.exit(1)

    config = H3YunConfig.from_env()
    client = H3YunClient(config)

    try:
        results = client.create_biz_objects(
            args.schema,
            biz_objects,
            is_submit=not args.draft,
            batch_size=args.batch_size
        )
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
