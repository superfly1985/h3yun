# -*- coding: utf-8 -*-
"""
氚云 API 自定义异常类
"""


class H3YunError(Exception):
    """氚云 API 基础异常"""

    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


class H3YunAuthError(H3YunError):
    """认证失败异常（EngineCode/Secret 错误）"""
    pass


class H3YunAPIError(H3YunError):
    """API 调用失败异常"""

    def __init__(self, message: str, response_data: dict = None, status_code: int = None):
        super().__init__(message)
        self.response_data = response_data or {}
        self.status_code = status_code


class H3YunValidationError(H3YunError):
    """参数验证失败异常"""
    pass


class H3YunNotFoundError(H3YunError):
    """资源不存在异常（记录、表单等）"""
    pass


class H3YunRateLimitError(H3YunError):
    """请求频率限制异常"""
    pass


class H3YunNetworkError(H3YunError):
    """网络请求异常"""
    pass
