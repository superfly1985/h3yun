# 氚云 (H3Yun) Python SDK

氚云平台的 Python SDK，提供完整的 API 操作支持。

> **注意：这是内部私有库，请勿上传到 PyPI 或其他公开仓库。**

## 功能特性

- ✅ 业务数据查询（单条/批量）
- ✅ 业务数据创建（单条/批量）
- ✅ 业务数据更新
- ✅ 业务数据删除
- ✅ 附件上传/下载
- ✅ 自动重试机制
- ✅ 完整的类型提示
- ✅ 自定义异常类

## 安装

### 方式1：通过 Git 安装（推荐）

```bash
# 通过 SSH
pip install git+ssh://git@your-git-server.com/path/to/h3yun-sdk.git

# 通过 HTTPS
pip install git+https://your-git-server.com/path/to/h3yun-sdk.git

# 安装指定版本
pip install git+ssh://git@your-git-server.com/path/to/h3yun-sdk.git@v0.1.0
```

### 方式2：在 requirements.txt 中指定

```txt
# requirements.txt
git+ssh://git@your-git-server.com/path/to/h3yun-sdk.git@v0.1.0
```

然后执行：
```bash
pip install -r requirements.txt
```

### 方式3：本地开发安装

```bash
git clone git@your-git-server.com:path/to/h3yun-sdk.git
cd h3yun-sdk
pip install -e .
```

### 方式4：复制源码使用

直接将 `src/h3yun/` 目录复制到你的项目中：

```
your-project/
├── h3yun/              # 复制 src/h3yun/ 到这里
│   ├── __init__.py
│   ├── config.py
│   ├── client.py
│   └── exceptions.py
└── your_code.py
```

## 快速开始

### 1. 配置环境变量

```bash
export H3YUN_ENGINE_CODE="your_engine_code"
export H3YUN_SECRET="your_secret"
export H3YUN_BASE_URL="https://www.h3yun.com"  # 可选，默认
export H3YUN_TIMEOUT="30"  # 可选，默认30秒
```

### 2. 基础用法

```python
from h3yun import H3YunConfig, H3YunClient

# 从环境变量读取配置
config = H3YunConfig.from_env()
client = H3YunClient(config)

# 查询单条数据
result = client.load_biz_object("SchemaCode", "BizObjectId")

# 创建数据
new_data = {"Name": "张三", "Age": 25}
result = client.create_biz_object("SchemaCode", new_data)

# 更新数据
update_data = {"Status": "已完成"}
result = client.update_biz_object("SchemaCode", "BizObjectId", update_data)

# 删除数据
result = client.remove_biz_object("SchemaCode", "BizObjectId")

# 上传附件
result = client.upload_attachment(
    "SchemaCode",
    "BizObjectId",
    "FilePropertyName",
    "/path/to/file.png"
)

# 下载附件
result = client.download_attachment("AttachmentId", out_dir="./downloads")
```

### 3. 批量操作

```python
# 批量创建（自动分批处理）
items = [
    {"Name": "张三", "Age": 25},
    {"Name": "李四", "Age": 30},
    # ... 更多数据
]
results = client.create_biz_objects("SchemaCode", items, batch_size=100)

# 批量查询
params = {
    "ToRowNum": 100,
    "Filter": '{"Type":"And","Matchers":[]}'
}
result = client.load_biz_objects("SchemaCode", params)
```

## 配置说明

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `H3YUN_ENGINE_CODE` | 是 | 引擎编码 |
| `H3YUN_SECRET` | 是 | 引擎密钥 |
| `H3YUN_BASE_URL` | 否 | API基础URL，默认 `https://www.h3yun.com` |
| `H3YUN_TIMEOUT` | 否 | 请求超时时间（秒），默认30 |

### 代码配置

```python
from h3yun import H3YunConfig, H3YunClient

# 直接配置
config = H3YunConfig(
    engine_code="your_code",
    secret="your_secret",
    base_url="https://www.h3yun.com",
    timeout=30
)
client = H3YunClient(config)

# 从字典配置
config = H3YunConfig.from_dict({
    "engine_code": "your_code",
    "secret": "your_secret"
})
```

## 异常处理

```python
from h3yun import (
    H3YunClient,
    H3YunConfig,
    H3YunAuthError,
    H3YunAPIError,
    H3YunNotFoundError,
    H3YunNetworkError,
)

config = H3YunConfig.from_env()
client = H3YunClient(config)

try:
    result = client.load_biz_object("SchemaCode", "BizObjectId")
except H3YunAuthError as e:
    print(f"认证失败: {e}")
except H3YunNotFoundError as e:
    print(f"记录不存在: {e}")
except H3YunAPIError as e:
    print(f"API错误: {e}")
except H3YunNetworkError as e:
    print(f"网络错误: {e}")
```

## 示例代码

详见 [examples/](examples/) 目录：

- `load_biz_object.py` - 查询单条数据
- `load_biz_objects.py` - 批量查询数据
- `create_biz_object.py` - 创建单条数据
- `create_biz_objects.py` - 批量创建数据
- `update_biz_object.py` - 更新数据
- `remove_biz_object.py` - 删除数据
- `upload_attachment.py` - 上传附件
- `download_attachment.py` - 下载附件

## 项目结构

```
01.氚云读写方法/
├── src/h3yun/          # SDK核心代码
│   ├── __init__.py     # 包入口
│   ├── config.py       # 配置管理
│   ├── client.py       # API客户端
│   └── exceptions.py   # 自定义异常
├── examples/           # 使用示例
├── tests/              # 测试文件
├── config/             # 配置文件示例
├── document/           # 文档
└── download/           # 下载文件目录
```

## 内部使用说明

### 在其他项目中使用

#### 方法1：Git 子模块（推荐）

```bash
# 在主项目中添加子模块
git submodule add git@your-git-server.com:path/to/h3yun-sdk.git libs/h3yun-sdk

# 安装
pip install -e libs/h3yun-sdk
```

#### 方法2：直接复制

将 `src/h3yun/` 复制到目标项目的任意位置，然后：

```python
import sys
sys.path.insert(0, "/path/to/h3yun")
from h3yun import H3YunConfig, H3YunClient
```

#### 方法3：私有 PyPI（如有）

如果有内部 PyPI 服务器：

```bash
pip install h3yun --index-url https://your-pypi-server.com/simple
```

## 开发

```bash
# 克隆仓库
git clone git@your-git-server.com:path/to/h3yun-sdk.git

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 版本历史

详见 [changelog.md](changelog.md)

## 注意事项

- **请勿将此库上传到公开仓库（GitHub/PyPI 等）**
- 包含公司敏感信息（EngineCode/Secret）的配置请妥善保管
- 建议定期更新依赖包版本
