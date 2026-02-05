import json
import time
from typing import Any, Dict, Optional

import requests

try:
    from .h3yun_config import H3YunConfig
except ImportError:
    from h3yun_config import H3YunConfig


class H3YunClient:
    def __init__(self, config: H3YunConfig):
        config.validate()
        self.cfg = config

    def _timestamp_ms(self) -> str:
        return str(int(time.time() * 1000))

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "EngineCode": self.cfg.engine_code,
            "EngineSecret": self.cfg.secret,
        }

    def _url(self) -> str:
        return f"{self.cfg.base_url.rstrip('/')}/OpenApi/Invoke"

    def invoke(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        body = {"ActionName": action}
        body.update(params or {})
        r = requests.post(self._url(), headers=self._headers(), json=body, timeout=self.cfg.timeout)
        r.raise_for_status()
        return r.json()

    def get_form_records(self, form_name: Optional[str] = None, query: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        name = form_name or self.cfg.form_name
        params = {self.cfg.class_key: name, "Query": query or {}}
        return self.invoke(self.cfg.read_action, params)

    def create_form_record(self, form_name: Optional[str], data: Dict[str, Any]) -> Dict[str, Any]:
        name = form_name or self.cfg.form_name
        params = {self.cfg.class_key: name, "Data": data}
        return self.invoke(self.cfg.write_action, params)

    def update_form_record(self, form_name: Optional[str], record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        name = form_name or self.cfg.form_name
        params = {self.cfg.class_key: name, "SchemaCode": name, "FormCode": name, "Id": record_id, "Data": data}
        return self.invoke(self.cfg.update_action, params)

    def load_biz_object(self, schema_code: str, biz_object_id: str) -> Dict[str, Any]:
        return self.invoke("LoadBizObject", {"SchemaCode": schema_code, "BizObjectId": biz_object_id})

    def load_biz_objects(self, schema_code: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        p = {"SchemaCode": schema_code}
        if params:
            p.update(params)
        return self.invoke("LoadBizObjects", p)

    def create_biz_object(self, schema_code: str, biz_object: Any, is_submit: bool = True) -> Dict[str, Any]:
        if isinstance(biz_object, str):
            biz_str = biz_object
        else:
            biz_str = json.dumps(biz_object, ensure_ascii=False, separators=(",", ":"))
        params = {"SchemaCode": schema_code, "BizObject": biz_str, "IsSubmit": "true" if is_submit else "false"}
        return self.invoke("CreateBizObject", params)

    def create_biz_objects(self, schema_code: str, biz_objects: Any, is_submit: bool = True) -> Dict[str, Any]:
        arr: list[str] = []
        if isinstance(biz_objects, str):
            try:
                parsed = json.loads(biz_objects)
                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, str):
                            arr.append(item)
                        else:
                            arr.append(json.dumps(item, ensure_ascii=False, separators=(",", ":")))
                else:
                    raise ValueError("biz_objects string must be a JSON array")
            except json.JSONDecodeError:
                raise ValueError("biz_objects must be a JSON array string")
        elif isinstance(biz_objects, list):
            for item in biz_objects:
                if isinstance(item, str):
                    arr.append(item)
                else:
                    arr.append(json.dumps(item, ensure_ascii=False, separators=(",", ":")))
        else:
            raise ValueError("biz_objects must be a list or JSON array string")

        params = {"SchemaCode": schema_code, "BizObjectArray": arr, "IsSubmit": "true" if is_submit else "false"}
        return self.invoke("CreateBizObjects", params)

    def update_biz_object(self, schema_code: str, biz_object_id: str, biz_object: Any) -> Dict[str, Any]:
        if isinstance(biz_object, str):
            biz_str = biz_object
        else:
            biz_str = json.dumps(biz_object, ensure_ascii=False, separators=(",", ":"))
        params = {"SchemaCode": schema_code, "BizObject": biz_str, "BizObjectId": biz_object_id}
        return self.invoke("UpdateBizObject", params)

    def remove_biz_object(self, schema_code: str, biz_object_id: str) -> Dict[str, Any]:
        return self.invoke("RemoveBizObject", {"SchemaCode": schema_code, "BizObjectId": biz_object_id})

    def upload_attachment(self, schema_code: str, biz_object_id: str, file_property_name: str, file_path: str, content_type: Optional[str] = None) -> Dict[str, Any]:
        import mimetypes
        ct = content_type or mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        url = f"{self.cfg.base_url.rstrip('/')}/OpenApi/UploadAttachment"
        params = {"SchemaCode": schema_code, "FilePropertyName": file_property_name, "BizObjectId": biz_object_id}
        name = file_path.split("/")[-1].split("\\")[-1]
        import time as _t
        boundary = "----------" + format(int(_t.time() * 1000), "x")
        pre = ("--" + boundary + "\r\n" + "Content-Disposition: form-data; name=\"media\"; filename=\"" + name + "\"\r\n" + "Content-Type: " + ct + "\r\n\r\n").encode("utf-8")
        end = ("\r\n--" + boundary + "--\r\n").encode("ascii")
        with open(file_path, "rb") as f:
            body = pre + f.read() + end
        headers = self._headers().copy()
        headers["Content-Type"] = "multipart/form-data; boundary=" + boundary
        r = requests.post(url, headers=headers, params=params, data=body, timeout=self.cfg.timeout)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"Raw": r.text, "StatusCode": r.status_code}

    def download_attachment(self, attachment_id: str, out_dir: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.cfg.base_url.rstrip('/')}/Api/DownloadBizObjectFile"
        data = {"attachmentId": attachment_id, "EngineCode": self.cfg.engine_code}
        headers = {"EngineCode": self.cfg.engine_code, "EngineSecret": self.cfg.secret}
        r = requests.post(url, data=data, headers=headers, timeout=self.cfg.timeout)
        r.raise_for_status()
        fname = None
        cd = r.headers.get("Content-Disposition") or r.headers.get("content-disposition")
        if cd:
            try:
                part = [p.strip() for p in cd.split(";")]
                for p in part:
                    if p.lower().startswith("filename="):
                        v = p.split("=", 1)[1].strip().strip('"')
                        fname = v
                        break
            except Exception:
                pass
        if not fname:
            fname = attachment_id + ".bin"
        import os
        d = out_dir or os.path.join(os.getcwd(), "Web_Service", "氚云", "download")
        os.makedirs(d, exist_ok=True)
        pth = os.path.join(d, fname)
        with open(pth, "wb") as f:
            f.write(r.content)
        return {"ok": True, "path": pth, "filename": fname, "size": len(r.content)}
