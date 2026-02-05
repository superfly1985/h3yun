import os
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from h3yun_config import H3YunConfig
from h3yun_client import H3YunClient


def run_smoke():
    os.environ["H3YUN_COMPANY"] = "长春科世得润汽车部件有限公司"
    os.environ["H3YUN_ENGINE_CODE"] = "te3huyefiy58eejx6li7kbac0"
    os.environ["H3YUN_SECRET"] = "1ZT/CAEmwURNmMhj3YnCflN4LdoSejNWQd+Rt6IF/iEuA3K/EvdyTw=="
    os.environ["H3YUN_FORM_NAME"] = "D287764relabel"
    cfg = H3YunConfig.from_env()
    client = H3YunClient(cfg)
    try:
        print("try read")
        read_res = client.invoke("GetFormData", {"ClassName": cfg.form_name, "Query": {}})
        print(json.dumps(read_res, ensure_ascii=False)[:500])
    except Exception as e:
        print("read_error", str(e))
    try:
        print("try write")
        write_res = client.invoke("SaveFormData", {"ClassName": cfg.form_name, "Data": {"_demo": "value"}})
        print(json.dumps(write_res, ensure_ascii=False)[:500])
    except Exception as e:
        print("write_error", str(e))


if __name__ == "__main__":
    run_smoke()
