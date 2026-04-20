# -*- coding: utf-8 -*-
"""
氚云 (H3Yun) OpenClaw Skill

版本: 1.1.4
"""
import os
from pathlib import Path

from h3yun import H3YunConfig, H3YunClient

__version__ = "1.1.4"


class H3YunSkill:
    VERSION = __version__
    
    def __init__(self, config: dict = None):
        skill_config = config or {}
        
        engine_code = skill_config.get("engine_code") or os.getenv("H3YUN_ENGINE_CODE")
        secret = skill_config.get("secret") or os.getenv("H3YUN_SECRET")
        base_url = skill_config.get("base_url") or os.getenv("H3YUN_BASE_URL") or "https://www.h3yun.com"
        timeout = skill_config.get("timeout") or int(os.getenv("H3YUN_TIMEOUT", "30"))
        
        if not engine_code:
            raise ValueError("缺少 engine_code，请在 Skill 配置中设置或设置环境变量 H3YUN_ENGINE_CODE")
        if not secret:
            raise ValueError("缺少 secret，请在 Skill 配置中设置或设置环境变量 H3YUN_SECRET")
        
        self.h3yun_config = H3YunConfig(
            engine_code=engine_code,
            secret=secret,
            base_url=base_url,
            timeout=timeout
        )
        self.client = H3YunClient(self.h3yun_config)

    def 查询单条业务数据(self, schema_code: str, biz_object_id: str):
        """
        根据表单编码和业务对象ID查询单条业务数据

        Args:
            schema_code: 表单编码 (SchemaCode)
            biz_object_id: 业务对象ID (ObjectId)
        
        Returns:
            {"success": True, "data": BizObject}
            BizObject 包含业务数据的完整字段
        """
        result = self.client.load_biz_object(schema_code, biz_object_id)
        # 提取业务数据，返回更友好的结构
        return_data = result.get("ReturnData", {})
        biz_object = return_data.get("BizObject", {}) if isinstance(return_data, dict) else {}
        return {"success": True, "data": biz_object}

    def 批量查询业务数据(self, schema_code: str, filter_field: str = None, 
                      filter_value: str = None, filter_operator: int = 2,
                      from_row_num: int = 0, to_row_num: int = 500):
        """
        批量查询业务数据，支持按字段条件过滤。默认返回前500条，最大500条。

        Args:
            schema_code: 表单编码 (SchemaCode)
            filter_field: 过滤字段名（以查询返回的实际字段名为准）
            filter_value: 过滤字段的值
            filter_operator: 过滤运算符，0=大于, 1=大于等于, 2=等于(默认), 3=小于等于,
                             4=小于, 5=不等于, 6=在范围内, 7=不在范围内
            from_row_num: 分页起始行号（从0开始）
            to_row_num: 分页结束行号（最大500）
        
        Returns:
            {"success": True, "data": {"BizObjectArray": [...], "TotalCount": N}}
        """
        matcher = None
        if filter_field and filter_value:
            matcher = {
                "Type": "And",
                "Matchers": [
                    {
                        "Type": "Item",
                        "Name": filter_field,
                        "Operator": filter_operator,
                        "Value": filter_value
                    }
                ]
            }
        
        result = self.client.load_biz_objects(
            schema_code,
            from_row_num=from_row_num,
            to_row_num=to_row_num,
            matcher=matcher
        )
        # 提取业务数据列表
        return_data = result.get("ReturnData", {})
        simplified = {
            "BizObjectArray": return_data.get("BizObjectArray", []) if isinstance(return_data, dict) else [],
            "TotalCount": return_data.get("TotalCount", 0) if isinstance(return_data, dict) else 0,
        }
        return {"success": True, "data": simplified}

    def 创建单条业务数据(self, schema_code: str, data: dict, is_submit: bool = True):
        """
        创建单条业务数据，可选择是否直接提交

        Args:
            schema_code: 表单编码 (SchemaCode)
            data: 业务数据，键为字段名（以查询返回的实际字段名为准）
            is_submit: 是否直接提交，True=提交(默认)，False=仅保存草稿
        
        Returns:
            {"success": True, "data": {"BizObjectId": "xxx"}}
        """
        result = self.client.create_biz_object(schema_code, data, is_submit=is_submit)
        # 提取创建的ID
        return_data = result.get("ReturnData", {})
        biz_id = return_data.get("BizObjectId") if isinstance(return_data, dict) else None
        return {"success": True, "data": {"BizObjectId": biz_id}}

    def 批量创建业务数据(self, schema_code: str, data_list: list, is_submit: bool = True):
        """
        批量创建业务数据，每次最多100条

        Args:
            schema_code: 表单编码 (SchemaCode)
            data_list: 业务数据列表，每个元素是一个字典（字段名: 值）
            is_submit: 是否直接提交，True=提交(默认)，False=仅保存草稿
        
        Returns:
            {"success": True, "data": {"created_count": N, "results": [...]}}
        """
        results = self.client.create_biz_objects(schema_code, data_list, is_submit=is_submit)
        # 统计创建成功的数量
        created_count = 0
        for result in results:
            return_data = result.get("ReturnData", {})
            if isinstance(return_data, dict) and return_data.get("Successful"):
                created_count += return_data.get("Count", 0)
        
        return {
            "success": True, 
            "data": {
                "created_count": created_count,
                "results": results
            }
        }

    def 更新业务数据(self, schema_code: str, biz_object_id: str, data: dict):
        """
        更新指定ID的业务数据

        Args:
            schema_code: 表单编码 (SchemaCode)
            biz_object_id: 业务对象ID (ObjectId)
            data: 更新数据，键为字段名，只需传需要更新的字段
        
        Returns:
            {"success": True, "data": {"BizObjectId": "xxx"}}
        """
        result = self.client.update_biz_object(schema_code, biz_object_id, data)
        return {"success": True, "data": {"BizObjectId": biz_object_id}}

    def 删除业务数据(self, schema_code: str, biz_object_id: str):
        """
        删除指定ID的业务数据（不可恢复）

        Args:
            schema_code: 表单编码 (SchemaCode)
            biz_object_id: 业务对象ID (ObjectId)
        
        Returns:
            {"success": True, "data": {"deleted": True}}
        """
        result = self.client.remove_biz_object(schema_code, biz_object_id)
        return {"success": True, "data": {"deleted": True}}

    def 上传附件(self, schema_code: str, biz_object_id: str, 
               field_name: str, file_path: str):
        """
        上传本地文件到氚云表单的附件字段

        Args:
            schema_code: 表单编码 (SchemaCode)
            biz_object_id: 业务对象ID (ObjectId)
            field_name: 附件字段的字段名（以查询返回的实际字段名为准）
            file_path: 本地文件的完整路径
        
        Returns:
            {"success": True, "data": {"AttachmentId": "xxx"}}
        """
        result = self.client.upload_attachment(
            schema_code, biz_object_id, field_name, file_path
        )
        # 提取附件ID
        attachment_id = result.get("AttachmentId") or result.get("ReturnData", {}).get("AttachmentId")
        return {"success": True, "data": {"AttachmentId": attachment_id}}

    def 下载附件(self, attachment_id: str, output_path: str = None):
        """
        根据附件ID从氚云下载附件到本地

        Args:
            attachment_id: 附件ID (AttachmentId)，如 fa5a96d4-559c-46c0-9dcc-dcb6e427a94c。
                           注意：不是URL，是附件的唯一标识ID。
            output_path: 保存目录路径（可选，默认保存到 ./download/ 目录）
        
        Returns:
            {"success": True, "data": {"file_path": "xxx", "filename": "xxx", "size": N}}
        """
        result = self.client.download_attachment(attachment_id, out_dir=output_path)
        # 简化返回结构
        return {
            "success": True, 
            "data": {
                "file_path": result.get("path"),
                "filename": result.get("filename"),
                "size": result.get("size"),
            }
        }


if __name__ == "__main__":
    try:
        skill = H3YunSkill()
        print(f"Skill v{H3YunSkill.VERSION} 初始化成功！")
    except Exception as e:
        print(f"Skill 初始化失败: {e}")
