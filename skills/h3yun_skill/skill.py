# -*- coding: utf-8 -*-
import os
from pathlib import Path

from h3yun import H3YunConfig, H3YunClient


class H3YunSkill:
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
        """
        result = self.client.load_biz_object(schema_code, biz_object_id)
        return {"success": True, "data": result}

    def 批量查询业务数据(self, schema_code: str, filter_field: str = None, 
                      filter_value: str = None, filter_operator: int = 2,
                      from_row_num: int = 0, to_row_num: int = 500):
        """
        批量查询业务数据，支持按字段条件过滤。默认返回前500条，最大500条。

        Args:
            schema_code: 表单编码 (SchemaCode)
            filter_field: 过滤字段编码（如 F0000002），不是字段标题
            filter_value: 过滤字段的值
            filter_operator: 过滤运算符，0=大于, 1=大于等于, 2=等于(默认), 3=小于等于,
                             4=小于, 5=不等于, 6=在范围内, 7=不在范围内
            from_row_num: 分页起始行号（从0开始）
            to_row_num: 分页结束行号（最大500）
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
        return {"success": True, "data": result}

    def 创建单条业务数据(self, schema_code: str, data: dict, is_submit: bool = True):
        """
        创建单条业务数据，可选择是否直接提交

        Args:
            schema_code: 表单编码 (SchemaCode)
            data: 业务数据，键为字段编码（如 F0000002），不是字段标题
            is_submit: 是否直接提交，True=提交(默认)，False=仅保存草稿
        """
        result = self.client.create_biz_object(schema_code, data, is_submit=is_submit)
        return {"success": True, "data": result}

    def 更新业务数据(self, schema_code: str, biz_object_id: str, data: dict):
        """
        更新指定ID的业务数据

        Args:
            schema_code: 表单编码 (SchemaCode)
            biz_object_id: 业务对象ID (ObjectId)
            data: 更新数据，键为字段编码（如 F0000002），只需传需要更新的字段
        """
        result = self.client.update_biz_object(schema_code, biz_object_id, data)
        return {"success": True, "data": result}

    def 删除业务数据(self, schema_code: str, biz_object_id: str):
        """
        删除指定ID的业务数据（不可恢复）

        Args:
            schema_code: 表单编码 (SchemaCode)
            biz_object_id: 业务对象ID (ObjectId)
        """
        result = self.client.remove_biz_object(schema_code, biz_object_id)
        return {"success": True, "data": result}

    def 上传附件(self, schema_code: str, biz_object_id: str, 
               field_name: str, file_path: str):
        """
        上传本地文件到氚云表单的附件字段

        Args:
            schema_code: 表单编码 (SchemaCode)
            biz_object_id: 业务对象ID (ObjectId)
            field_name: 附件字段的字段编码（如 F0000011），不是字段标题
            file_path: 本地文件的完整路径
        """
        result = self.client.upload_attachment(
            schema_code, biz_object_id, field_name, file_path
        )
        return {"success": True, "data": result}

    def 下载附件(self, attachment_id: str, output_path: str = None):
        """
        根据附件ID从氚云下载附件到本地

        Args:
            attachment_id: 附件ID (AttachmentId)，如 fa5a96d4-559c-46c0-9dcc-dcb6e427a94c。
                           注意：不是URL，是附件的唯一标识ID。
            output_path: 保存目录路径（可选，默认保存到 ./download/ 目录）
        """
        result = self.client.download_attachment(attachment_id, output_path)
        return {"success": True, "data": result}


if __name__ == "__main__":
    try:
        skill = H3YunSkill()
        print("Skill 初始化成功！")
    except Exception as e:
        print(f"Skill 初始化失败: {e}")
