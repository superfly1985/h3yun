# -*- coding: utf-8 -*-
"""
氚云 (H3Yun) API Python SDK

提供对氚云平台的API操作支持，包括：
- 业务数据查询（单条/批量）
- 业务数据创建（单条/批量）
- 业务数据更新
- 业务数据删除
- 附件上传/下载

基本用法:
    >>> from h3yun import H3YunConfig, H3YunClient
    >>> config = H3YunConfig.from_env()  # 从环境变量读取配置
    >>> client = H3YunClient(config)
    >>> result = client.load_biz_object("SchemaCode", "BizObjectId")
"""

__version__ = "1.1.4"
__author__ = "H3Yun SDK"

from .config import H3YunConfig
from .client import H3YunClient
from .exceptions import (
    H3YunError,
    H3YunAuthError,
    H3YunAPIError,
    H3YunValidationError,
    H3YunNotFoundError,
    H3YunRateLimitError,
)

__all__ = [
    "H3YunConfig",
    "H3YunClient",
    "H3YunError",
    "H3YunAuthError",
    "H3YunAPIError",
    "H3YunValidationError",
    "H3YunNotFoundError",
    "H3YunRateLimitError",
]
