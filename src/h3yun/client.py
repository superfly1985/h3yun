# -*- coding: utf-8 -*-
"""
氚云 API 客户端
"""
import json
import logging
import mimetypes
import os
import time
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import H3YunConfig
from .exceptions import (
    H3YunAPIError,
    H3YunAuthError,
    H3YunNetworkError,
    H3YunNotFoundError,
    H3YunValidationError,
)

logger = logging.getLogger(__name__)


class H3YunClient:
    """
    氚云 API 客户端

    提供对氚云 OpenAPI 的完整访问支持。

    Example:
        >>> from h3yun import H3YunConfig, H3YunClient
        >>> config = H3YunConfig(
        ...     engine_code="your_code",
        ...     secret="your_secret"
        ... )
        >>> client = H3YunClient(config)
        >>> result = client.load_biz_object("SchemaCode", "BizObjectId")
    """

    def __init__(
        self,
        config: H3YunConfig,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        """
        初始化客户端

        Args:
            config: 配置对象
            max_retries: 最大重试次数，默认3次
            backoff_factor: 重试间隔因子，默认0.5秒
        """
        self.cfg = config
        self.session = requests.Session()

        # 配置重试策略
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        logger.debug(f"H3YunClient initialized with base_url: {self.cfg.base_url}")

    def _headers(self) -> Dict[str, str]:
        """构建请求头"""
        return {
            "Content-Type": "application/json",
            "EngineCode": self.cfg.engine_code,
            "EngineSecret": self.cfg.secret,
        }

    def _invoke_url(self) -> str:
        """获取 Invoke API URL"""
        return f"{self.cfg.base_url.rstrip('/')}/OpenApi/Invoke"

    def invoke(self, action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        调用 OpenApi/Invoke 接口

        Args:
            action: 动作名称
            params: 请求参数

        Returns:
            API 响应数据

        Raises:
            H3YunAPIError: API 调用失败
            H3YunAuthError: 认证失败
            H3YunNetworkError: 网络请求失败
        """
        body = {"ActionName": action}
        if params:
            body.update(params)

        logger.debug(f"Invoke {action} with params: {params}")

        try:
            response = self.session.post(
                self._invoke_url(),
                headers=self._headers(),
                json=body,
                timeout=self.cfg.timeout,
            )
            response.raise_for_status()
            data = response.json()

            # 检查业务错误
            if not data.get("Successful", True):
                error_msg = data.get("ErrorMessage", "Unknown error")
                logger.error(f"API business error: {error_msg}")
                raise H3YunAPIError(error_msg, response_data=data)

            logger.debug(f"Invoke {action} success")
            return data

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise H3YunAuthError("认证失败，请检查 EngineCode 和 Secret") from e
            raise H3YunAPIError(f"HTTP {response.status_code}: {e}", status_code=response.status_code) from e
        except requests.exceptions.RequestException as e:
            raise H3YunNetworkError(f"网络请求失败: {e}") from e

    def load_biz_object(self, schema_code: str, biz_object_id: str) -> Dict[str, Any]:
        """
        查询单条业务数据

        Args:
            schema_code: 表单编码
            biz_object_id: 业务对象ID

        Returns:
            API 响应数据

        Raises:
            H3YunNotFoundError: 记录不存在
        """
        result = self.invoke("LoadBizObject", {
            "SchemaCode": schema_code,
            "BizObjectId": biz_object_id,
        })

        if not result.get("Successful"):
            error_msg = result.get("ErrorMessage", "")
            if "不存在" in error_msg or "not found" in error_msg.lower():
                raise H3YunNotFoundError(f"业务对象不存在: {biz_object_id}")

        return result

    @staticmethod
    def build_filter(
        from_row_num: int = 0,
        to_row_num: int = 500,
        matcher: Optional[Dict[str, Any]] = None,
        return_items: Optional[List[str]] = None,
        sort_by_collection: Optional[List[Dict[str, Any]]] = None,
        require_count: bool = False,
    ) -> str:
        """
        构建 LoadBizObjects 的 Filter 参数（符合官方规范）

        官方文档: https://help.h3yun.com/contents/1007/1633.html

        Args:
            from_row_num: 分页起始行，默认0
            to_row_num: 分页结束行，默认500（最大500）
            matcher: 查询条件，结构为 {"Type": "And", "Matchers": [...]}
                     单条件: {"Type": "Item", "Name": "字段名", "Operator": 2, "Value": "值"}
                     组合条件: {"Type": "And/Or", "Matchers": [子条件...]}
            return_items: 返回字段列表，不填返回所有字段
            sort_by_collection: 排序字段（官方暂不支持，默认置空）
            require_count: 是否查询总行数，默认False

        Returns:
            Filter JSON 字符串

        Example:
            >>> # 无条件查询前500条
            >>> f = H3YunClient.build_filter()
            >>> # 带条件查询
            >>> f = H3YunClient.build_filter(
            ...     to_row_num=100,
            ...     matcher={
            ...         "Type": "And",
            ...         "Matchers": [
            ...             {"Type": "Item", "Name": "F0000002", "Operator": 2, "Value": "123"}
            ...         ]
            ...     }
            ... )
        """
        filter_dict: Dict[str, Any] = {
            "FromRowNum": from_row_num,
            "ToRowNum": to_row_num,
            "RequireCount": require_count,
            "ReturnItems": return_items or [],
            "SortByCollection": sort_by_collection or [],
            "Matcher": matcher or {"Type": "And", "Matchers": []},
        }
        return json.dumps(filter_dict, ensure_ascii=False)

    def load_biz_objects(
        self,
        schema_code: str,
        filter_str: Optional[str] = None,
        from_row_num: int = 0,
        to_row_num: int = 500,
        matcher: Optional[Dict[str, Any]] = None,
        return_items: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        批量查询业务数据

        官方文档: https://help.h3yun.com/contents/1007/1633.html
        最大一次性加载500条数据。

        Args:
            schema_code: 表单编码
            filter_str: 完整的 Filter JSON 字符串（优先级最高，传入后忽略其他参数）
            from_row_num: 分页起始行，默认0
            to_row_num: 分页结束行，默认500
            matcher: 查询条件，结构为 {"Type": "And", "Matchers": [...]}
                     Operator: 0=大于, 1=大于等于, 2=等于, 3=小于等于, 4=小于, 5=不等于, 6=在范围内, 7=不在范围内
            return_items: 返回字段列表，不填返回所有字段

        Returns:
            API 响应数据

        Example:
            >>> # 无条件查询前500条
            >>> result = client.load_biz_objects("SchemaCode")
            >>> # 带条件查询
            >>> result = client.load_biz_objects(
            ...     "SchemaCode",
            ...     to_row_num=100,
            ...     matcher={
            ...         "Type": "And",
            ...         "Matchers": [
            ...             {"Type": "Item", "Name": "F0000002", "Operator": 2, "Value": "123"}
            ...         ]
            ...     }
            ... )
            >>> # 使用完整 Filter 字符串
            >>> result = client.load_biz_objects(
            ...     "SchemaCode",
            ...     filter_str=H3YunClient.build_filter(to_row_num=100)
            ... )
        """
        if filter_str is None:
            filter_str = self.build_filter(
                from_row_num=from_row_num,
                to_row_num=to_row_num,
                matcher=matcher,
                return_items=return_items,
            )
        return self.invoke("LoadBizObjects", {
            "SchemaCode": schema_code,
            "Filter": filter_str,
        })

    def create_biz_object(
        self,
        schema_code: str,
        biz_object: Union[Dict[str, Any], str],
        is_submit: bool = True,
    ) -> Dict[str, Any]:
        """
        创建单条业务数据

        Args:
            schema_code: 表单编码
            biz_object: 业务数据（字典或JSON字符串）
            is_submit: 是否提交，默认True

        Returns:
            API 响应数据
        """
        if isinstance(biz_object, dict):
            biz_str = json.dumps(biz_object, ensure_ascii=False, separators=(",", ":"))
        else:
            biz_str = biz_object

        return self.invoke("CreateBizObject", {
            "SchemaCode": schema_code,
            "BizObject": biz_str,
            "IsSubmit": "true" if is_submit else "false",
        })

    def create_biz_objects(
        self,
        schema_code: str,
        biz_objects: Union[List[Union[Dict[str, Any], str]], str],
        is_submit: bool = True,
        batch_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        批量创建业务数据

        Args:
            schema_code: 表单编码
            biz_objects: 业务数据列表（每个元素可以是字典或JSON字符串）
            is_submit: 是否提交，默认True
            batch_size: 每批处理数量，默认100条

        Returns:
            各批次API响应数据列表
        """
        # 解析输入数据
        if isinstance(biz_objects, str):
            parsed = json.loads(biz_objects)
            if not isinstance(parsed, list):
                raise H3YunValidationError("biz_objects 字符串必须是JSON数组")
            items = parsed
        else:
            items = biz_objects

        # 转换为JSON字符串
        arr: List[str] = []
        for item in items:
            if isinstance(item, dict):
                arr.append(json.dumps(item, ensure_ascii=False, separators=(",", ":")))
            else:
                arr.append(item)

        # 分批处理
        results = []
        for i in range(0, len(arr), batch_size):
            batch = arr[i:i + batch_size]
            logger.info(f"Creating batch {i // batch_size + 1}/{(len(arr) + batch_size - 1) // batch_size}, size: {len(batch)}")

            result = self.invoke("CreateBizObjects", {
                "SchemaCode": schema_code,
                "BizObjectArray": batch,
                "IsSubmit": "true" if is_submit else "false",
            })
            results.append(result)

        return results

    def update_biz_object(
        self,
        schema_code: str,
        biz_object_id: str,
        biz_object: Union[Dict[str, Any], str],
    ) -> Dict[str, Any]:
        """
        更新业务数据

        Args:
            schema_code: 表单编码
            biz_object_id: 业务对象ID
            biz_object: 业务数据（字典或JSON字符串）

        Returns:
            API 响应数据
        """
        if isinstance(biz_object, dict):
            biz_str = json.dumps(biz_object, ensure_ascii=False, separators=(",", ":"))
        else:
            biz_str = biz_object

        return self.invoke("UpdateBizObject", {
            "SchemaCode": schema_code,
            "BizObject": biz_str,
            "BizObjectId": biz_object_id,
        })

    def remove_biz_object(self, schema_code: str, biz_object_id: str) -> Dict[str, Any]:
        """
        删除业务数据

        Args:
            schema_code: 表单编码
            biz_object_id: 业务对象ID

        Returns:
            API 响应数据
        """
        return self.invoke("RemoveBizObject", {
            "SchemaCode": schema_code,
            "BizObjectId": biz_object_id,
        })

    def upload_attachment(
        self,
        schema_code: str,
        biz_object_id: str,
        file_property_name: str,
        file_path: str,
        content_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        上传附件

        Args:
            schema_code: 表单编码
            biz_object_id: 业务对象ID
            file_property_name: 文件属性名
            file_path: 本地文件路径
            content_type: 文件MIME类型，自动检测

        Returns:
            API 响应数据，包含 AttachmentId
        """
        ct = content_type or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        url = f"{self.cfg.base_url.rstrip('/')}/OpenApi/UploadAttachment"
        params = {
            "SchemaCode": schema_code,
            "FilePropertyName": file_property_name,
            "BizObjectId": biz_object_id,
        }

        filename = os.path.basename(file_path)
        boundary = f"----------{int(time.time() * 1000):x}"

        with open(file_path, "rb") as f:
            file_content = f.read()

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
            f"Content-Type: {ct}\r\n\r\n"
        ).encode("utf-8") + file_content + f"\r\n--{boundary}--\r\n".encode("ascii")

        headers = self._headers().copy()
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"

        logger.debug(f"Uploading attachment: {filename} ({len(file_content)} bytes)")

        try:
            response = self.session.post(
                url,
                headers=headers,
                params=params,
                data=body,
                timeout=self.cfg.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise H3YunNetworkError(f"上传附件失败: {e}") from e

    def download_attachment(
        self,
        attachment_id: str,
        out_dir: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        下载附件

        Args:
            attachment_id: 附件ID
            out_dir: 输出目录，默认当前目录下的 download/
            filename: 指定文件名，默认从响应头解析

        Returns:
            包含下载文件信息的字典
        """
        url = f"{self.cfg.base_url.rstrip('/')}/Api/DownloadBizObjectFile"
        data = {"attachmentId": attachment_id, "EngineCode": self.cfg.engine_code}
        headers = {
            "EngineCode": self.cfg.engine_code,
            "EngineSecret": self.cfg.secret,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        logger.debug(f"Downloading attachment: {attachment_id}")

        try:
            response = self.session.post(
                url,
                data=data,
                headers=headers,
                timeout=self.cfg.timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise H3YunNetworkError(f"下载附件失败: {e}") from e

        # 解析文件名
        fname = filename
        if not fname:
            cd = response.headers.get("Content-Disposition") or response.headers.get("content-disposition")
            if cd:
                for part in cd.split(";"):
                    part = part.strip()
                    if part.lower().startswith("filename="):
                        fname = part.split("=", 1)[1].strip().strip('"')
                        break

        if not fname:
            fname = f"{attachment_id}.bin"

        # 确定输出目录
        output_dir = out_dir or os.path.join(os.getcwd(), "download")
        os.makedirs(output_dir, exist_ok=True)

        file_path = os.path.join(output_dir, fname)
        with open(file_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Attachment downloaded: {file_path} ({len(response.content)} bytes)")

        return {
            "ok": True,
            "path": file_path,
            "filename": fname,
            "size": len(response.content),
        }
