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
        result = self.client.load_biz_object(schema_code, biz_object_id)
        return {"success": True, "data": result}

    def 批量查询业务数据(self, schema_code: str, filter_field: str = None, 
                      filter_value: str = None, page_index: int = 1, 
                      page_size: int = 20):
        params = {
            "ToRowNum": page_size,
        }
        
        if filter_field and filter_value:
            import json
            filter_data = {
                "Type": "And",
                "ChildItems": [
                    {
                        "Type": "Item",
                        "Name": filter_field,
                        "Operator": 2,
                        "Value": filter_value
                    }
                ]
            }
            params["Filter"] = json.dumps(filter_data, ensure_ascii=False, separators=(",", ":"))
        
        result = self.client.load_biz_objects(schema_code, params)
        return {"success": True, "data": result}

    def 创建单条业务数据(self, schema_code: str, data: dict):
        result = self.client.create_biz_object(schema_code, data)
        return {"success": True, "data": result}

    def 更新业务数据(self, schema_code: str, biz_object_id: str, data: dict):
        result = self.client.update_biz_object(schema_code, biz_object_id, data)
        return {"success": True, "data": result}

    def 删除业务数据(self, schema_code: str, biz_object_id: str):
        result = self.client.remove_biz_object(schema_code, biz_object_id)
        return {"success": True, "data": result}

    def 上传附件(self, schema_code: str, biz_object_id: str, 
               field_name: str, file_path: str):
        result = self.client.upload_attachment(
            schema_code, biz_object_id, field_name, file_path
        )
        return {"success": True, "data": result}

    def 下载附件(self, attachment_url: str, output_path: str = None):
        saved_path = self.client.download_attachment(attachment_url, output_path)
        return {"success": True, "file_path": str(saved_path)}


if __name__ == "__main__":
    try:
        skill = H3YunSkill()
        print("Skill 初始化成功！")
    except Exception as e:
        print(f"Skill 初始化失败: {e}")
