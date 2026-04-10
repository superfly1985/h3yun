# -*- coding: utf-8 -*-
"""
示例：批量查询业务数据

Usage:
    python examples/load_biz_objects.py --schema SchemaCode [--filter filter.json]

Example:
    python examples/load_biz_objects.py --schema D000001test
    python examples/load_biz_objects.py --schema D000001test --filter config/filter.example.json
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

    parser = argparse.ArgumentParser(description="批量查询业务数据")
    parser.add_argument("--schema", required=True, help="表单编码 (SchemaCode)")
    parser.add_argument("--filter", help="过滤条件JSON文件路径")
    parser.add_argument("--top", type=int, default=100, help="返回记录数上限，默认100")
    args = parser.parse_args()

    config = H3YunConfig.from_env()
    client = H3YunClient(config)

    # 构建查询参数
    params = {"ToRowNum": args.top}

    if args.filter:
        with open(args.filter, "r", encoding="utf-8") as f:
            filter_data = json.load(f)
        params["Filter"] = json.dumps(filter_data, ensure_ascii=False, separators=(",", ":"))

    try:
        result = client.load_biz_objects(args.schema, params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
