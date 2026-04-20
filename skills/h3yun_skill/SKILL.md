---
name: h3yun
description: 读写氚云 (H3Yun) 平台的业务数据，支持增删改查、附件上传下载。当用户提到氚云、H3Yun、业务数据、表单操作、查询表单、创建数据、更新记录、删除数据、上传附件、下载附件时触发。
---

# 氚云 (H3Yun) 数据操作技能

## 配置

```json
{
  "engine_code": "你的EngineCode",
  "secret": "你的Secret",
  "base_url": "https://www.h3yun.com",
  "timeout": 30
}
```

或环境变量：`H3YUN_ENGINE_CODE`, `H3YUN_SECRET`

---

## 字段名称说明

氚云表单字段有三种命名方式，**以查询返回的实际 JSON 键名为准**：

| 类型 | 示例 |
|------|------|
| 固有字段 | `ObjectId`, `Name`, `CreatedBy`, `CreatedTime` |
| 自动字段 | `F0000002`, `F0000003`（系统自动生成） |
| 自定义字段 | `UserName`, `Password`, `部门`（用户自定义） |

**获取字段名方法**：先用`批量查询业务数据`查一条数据，返回的 JSON 键名即为字段名。

---

## Actions

### 查询单条业务数据

根据表单编码和业务对象ID查询单条数据。

**参数：**
- `schema_code`: 表单编码 (SchemaCode)
- `biz_object_id`: 业务对象ID (ObjectId)

**返回：**
```json
{
  "success": true,
  "data": {
    "ObjectId": "xxx",
    "Name": "数据标题",
    "字段名": "值"
  }
}
```

---

### 批量查询业务数据

批量查询业务数据，支持条件过滤和分页。

**参数：**
- `schema_code`: 表单编码
- `filter_field`: 过滤字段名（可选）
- `filter_value`: 过滤值（可选）
- `filter_operator`: 过滤运算符：0=大于, 1=大于等于, 2=等于(默认), 3=小于等于, 4=小于, 5=不等于, 6=在范围内, 7=不在范围内
- `from_row_num`: 起始行号（从0开始，默认0）
- `to_row_num`: 结束行号（最大500，默认500）

**返回：**
```json
{
  "success": true,
  "data": {
    "BizObjectArray": [{...}, {...}],
    "TotalCount": 100
  }
}
```

---

### 创建单条业务数据

创建业务数据，可选择直接提交或保存草稿。

**参数：**
- `schema_code`: 表单编码
- `data`: 业务数据对象，键为字段名
- `is_submit`: 是否直接提交，true(默认)=提交，false=保存草稿

**返回：**
```json
{
  "success": true,
  "data": {"BizObjectId": "xxx"}
}
```

**示例：**
```python
skill.创建单条业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    data={"F0000002": "张三", "F0000003": "技术部"},
    is_submit=True
)
```

---

### 批量创建业务数据

批量创建多条业务数据，每次最多100条，超过会自动分批处理。

**参数：**
- `schema_code`: 表单编码
- `data_list`: 业务数据列表，每个元素是一个对象
- `is_submit`: 是否直接提交，true(默认)=提交，false=保存草稿

**返回：**
```json
{
  "success": true,
  "data": {
    "created_count": 2,
    "results": [...]
  }
}
```

**示例：**
```python
skill.批量创建业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    data_list=[
        {"F0000002": "张三", "F0000003": "技术部"},
        {"F0000002": "李四", "F0000003": "销售部"}
    ],
    is_submit=True
)
```

---

### 更新业务数据

更新指定ID的业务数据。

**参数：**
- `schema_code`: 表单编码
- `biz_object_id`: 业务对象ID
- `data`: 更新数据，只需传需要更新的字段

**返回：**
```json
{"success": true, "data": {"BizObjectId": "xxx"}}
```

---

### 删除业务数据

删除指定ID的业务数据（不可恢复）。

**参数：**
- `schema_code`: 表单编码
- `biz_object_id`: 业务对象ID

**返回：**
```json
{"success": true, "data": {"deleted": true}}
```

---

### 上传附件

上传本地文件到氚云表单的附件字段。

**参数：**
- `schema_code`: 表单编码
- `biz_object_id`: 业务对象ID
- `field_name`: 附件字段名
- `file_path`: 本地文件完整路径

**返回：**
```json
{"success": true, "data": {"AttachmentId": "xxx"}}
```

---

### 下载附件

根据附件ID下载附件到本地。

**参数：**
- `attachment_id`: 附件ID（不是URL）
- `output_path`: 保存目录路径（可选，默认./download/）

**返回：**
```json
{
  "success": true,
  "data": {
    "file_path": "D:/download/filename.pdf",
    "filename": "filename.pdf",
    "size": 1024
  }
}
```

---

## 版本

v1.1.4
