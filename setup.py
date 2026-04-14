# -*- coding: utf-8 -*-
"""
氚云 (H3Yun) Python SDK - 内部私有库

安装方式:
    1. 直接安装: pip install git+ssh://git@github.com/superfly1985/h3yun.git
    2. 本地安装: pip install -e .
    3. requirements.txt: git+ssh://git@github.com/superfly1985/h3yun.git@v1.1.0

OpenClaw Skill:
    直接使用 skills/h3yun_skill/ 文件夹作为 OpenClaw 技能
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="h3yun",
    version="1.1.0",
    author="Your Company",
    author_email="",
    description="氚云 (H3Yun) API Python SDK - 内部使用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/superfly1985/h3yun",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Private :: Do Not Upload",  # 标记为私有，防止误上传 PyPI
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
    },
    # 不设置 entry_points，避免与其他包冲突
)
