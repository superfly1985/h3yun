# -*- coding: utf-8 -*-
"""
氚云 API 配置管理
"""
import os
import re
from dataclasses import dataclass, field
from typing import Optional
from .exceptions import H3YunValidationError


def _load_dotenv(path: str = ".env") -> None:
    """
    加载 .env 文件到环境变量（已存在的环境变量优先，不覆盖）

    Args:
        path: .env 文件路径，默认当前工作目录下的 .env
    """
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # 去掉成对引号和行内注释
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            elif " #" in value:
                value = value.split(" #", 1)[0].strip()
            if key and key not in os.environ:
                os.environ[key] = value


@dataclass
class H3YunConfig:
    """
    氚云 API 配置类

    Attributes:
        engine_code: 引擎编码（必填）
        secret: 引擎密钥（必填）
        base_url: API基础URL，默认 https://www.h3yun.com
        timeout: 请求超时时间（秒），默认30
        company_name: 公司名称（可选）
    """

    engine_code: str
    secret: str
    base_url: str = "https://www.h3yun.com"
    timeout: int = 30
    company_name: Optional[str] = None

    def __post_init__(self):
        """初始化后验证"""
        self.validate()

    def validate(self) -> None:
        """
        验证配置是否有效

        Raises:
            H3YunValidationError: 配置验证失败
        """
        errors = []

        if not self.engine_code:
            errors.append("engine_code 不能为空")
        elif not re.match(r'^[A-Za-z0-9_-]+$', self.engine_code):
            errors.append(f"engine_code 格式无效: {self.engine_code}")

        if not self.secret:
            errors.append("secret 不能为空")
        elif len(self.secret) < 10:
            errors.append("secret 长度不足，请检查配置")

        if not self.base_url:
            errors.append("base_url 不能为空")
        elif not self.base_url.startswith(("http://", "https://")):
            errors.append(f"base_url 必须以 http:// 或 https:// 开头: {self.base_url}")

        if self.timeout < 1 or self.timeout > 300:
            errors.append(f"timeout 必须在 1-300 秒之间: {self.timeout}")

        if errors:
            raise H3YunValidationError("配置验证失败: " + "; ".join(errors))

    @classmethod
    def from_env(cls, prefix: str = "H3YUN_") -> "H3YunConfig":
        """
        从环境变量读取配置（自动加载当前工作目录下的 .env 文件，已存在的环境变量优先）

        Args:
            prefix: 环境变量前缀，默认 H3YUN_

        Returns:
            H3YunConfig: 配置实例

        Raises:
            H3YunValidationError: 配置验证失败

        Example:
            >>> # 方式1: 项目根目录放 .env 文件 (参考 .env.example)
            >>> config = H3YunConfig.from_env()
            >>> # 方式2: 设置环境变量
            >>> import os
            >>> os.environ["H3YUN_ENGINE_CODE"] = "your_code"
            >>> os.environ["H3YUN_SECRET"] = "your_secret"
            >>> config = H3YunConfig.from_env()
        """
        _load_dotenv()
        return cls(
            engine_code=os.getenv(f"{prefix}ENGINE_CODE", ""),
            secret=os.getenv(f"{prefix}SECRET", ""),
            base_url=os.getenv(f"{prefix}BASE_URL", "https://www.h3yun.com"),
            timeout=int(os.getenv(f"{prefix}TIMEOUT", "30")),
            company_name=os.getenv(f"{prefix}COMPANY_NAME"),
        )

    @classmethod
    def from_dict(cls, data: dict) -> "H3YunConfig":
        """
        从字典创建配置

        Args:
            data: 配置字典

        Returns:
            H3YunConfig: 配置实例
        """
        return cls(
            engine_code=data.get("engine_code", ""),
            secret=data.get("secret", ""),
            base_url=data.get("base_url", "https://www.h3yun.com"),
            timeout=data.get("timeout", 30),
            company_name=data.get("company_name"),
        )
