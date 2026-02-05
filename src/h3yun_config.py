import os
from dataclasses import dataclass


@dataclass
class H3YunConfig:
    company_name: str
    engine_code: str
    secret: str
    form_name: str
    base_url: str
    read_action: str
    write_action: str
    update_action: str
    class_key: str
    timeout: int

    @staticmethod
    def from_env() -> "H3YunConfig":
        return H3YunConfig(
            company_name=os.getenv("H3YUN_COMPANY", ""),
            engine_code=os.getenv("H3YUN_ENGINE_CODE", ""),
            secret=os.getenv("H3YUN_SECRET", ""),
            form_name=os.getenv("H3YUN_FORM_NAME", ""),
            base_url=os.getenv("H3YUN_BASE_URL", "https://www.h3yun.com"),
            read_action=os.getenv("H3YUN_READ_ACTION", "LoadBizObjects"),
            write_action=os.getenv("H3YUN_WRITE_ACTION", "SaveFormData"),
            update_action=os.getenv("H3YUN_UPDATE_ACTION", "UpdateFormData"),
            class_key=os.getenv("H3YUN_CLASS_KEY", "SchemaCode"),
            timeout=int(os.getenv("H3YUN_TIMEOUT", "30")),
        )

    def validate(self) -> None:
        missing = []
        if not self.engine_code:
            missing.append("H3YUN_ENGINE_CODE")
        if not self.secret:
            missing.append("H3YUN_SECRET")
        if missing:
            raise ValueError("Missing required environment variables: " + ",".join(missing))
