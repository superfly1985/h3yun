# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "skills" / "h3yun_skill"))
sys.path.insert(0, str(project_root / "src"))

from skill import H3YunSkill


def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and "=" in s and not s.startswith("#"):
                k, v = s.split("=", 1)
                os.environ[k.strip()] = v.strip()


def test_skill():
    print("=" * 60)
    print("测试氚云 OpenClaw Skill")
    print("=" * 60)
    
    load_env()
    
    print("\n1. 初始化 Skill（从环境变量读取）...")
    try:
        skill = H3YunSkill()
        print("   ✅ Skill 初始化成功！")
    except Exception as e:
        print(f"   ❌ Skill 初始化失败: {e}")
        print("\n提示：请确保已设置环境变量或在 OpenClaw 中配置 Skill")
        return False
    
    print("\n✅ Skill 测试通过！")
    print("\n提示：实际使用时，在 OpenClaw 中配置 Skill 或设置环境变量即可")
    return True


if __name__ == "__main__":
    success = test_skill()
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试通过！")
    else:
        print("❌ 测试失败！")
    print("=" * 60)
