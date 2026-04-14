# -*- coding: utf-8 -*-
"""
氚云 API 配置管理
"""
import os
import re
from dataclasses import dataclass, field
from typing import Optional
from .exceptions import H3YunValidationError


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
        从环境变量读取配置

        Args:
            prefix: 环境变量前缀，默认 H3YUN_

        Returns:
            H3YunConfig: 配置实例

        Raises:
            H3YunValidationError: 配置验证失败

        Example:
            >>> # 设置环境变量
            >>> import os
            >>> os.environ["H3YUN_ENGINE_CODE"] = "your_code"
            >>> os.environ["H3YUN_SECRET"] = "your_secret"
            >>> config = H3YunConfig.from_env()
        """
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
