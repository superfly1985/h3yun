# 氚云 (H3Yun) OpenClaw Skill

## 功能说明

该 Skill 提供了与氚云平台集成的能力，支持：

| 功能 | 说明 |
|------|------|
| 查询单条业务数据 | 根据 SchemaCode 和 ObjectId 查询单条数据 |
| 批量查询业务数据 | 支持按字段条件过滤、分页查询（最大500条） |
| 创建单条业务数据 | 新增一条业务数据，可选提交或保存草稿 |
| 更新业务数据 | 更新指定 ID 的业务数据 |
| 删除业务数据 | 删除指定 ID 的业务数据（不可恢复） |
| 上传附件 | 上传文件到氚云表单的附件字段 |
| 下载附件 | 根据附件ID下载附件到本地 |

## 配置方式

### 方式 1：OpenClaw Skill 配置（推荐）

在 OpenClaw 中配置 Skill 时填写：

```json
{
  "engine_code": "你的EngineCode",
  "secret": "你的Secret",
  "base_url": "https://www.h3yun.com",
  "timeout": 30
}
```

### 方式 2：环境变量

设置以下环境变量：

```bash
H3YUN_ENGINE_CODE=你的EngineCode
H3YUN_SECRET=你的Secret
H3YUN_BASE_URL=https://www.h3yun.com
H3YUN_TIMEOUT=30
```

### 优先级

OpenClaw 配置 > 环境变量 > 默认值

## 重要：字段编码 vs 字段标题

氚云 API 使用**字段编码**（如 `F0000002`），不是字段标题（如"客户名称"）。

### 如何获取字段编码

**方式 1：通过 API 查询（推荐）**

先用 `批量查询业务数据` 查询一条数据，返回的 JSON 键名就是字段编码：

```json
{
  "ObjectId": "xxx",
  "F0000002": "张三",
  "F0000003": "技术部"
}
```

**方式 2：在表单设计器中查看**

1. 进入表单设计器
2. 选中任意字段
3. 在右侧属性面板查看**字段编码**（不是字段标题）

### 如何获取表单编码 (SchemaCode)

1. 登录氚云管理后台
2. 进入 **应用管理** → 选择你的应用
3. 找到需要操作的表单，点击 **设置**
4. 在表单设置页面可以看到 **表单编码 (SchemaCode)**

## 使用示例

### 查询单条数据

```python
skill.查询单条业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    biz_object_id="09a980d8-3b80-4f08-bbbd-732e0afa40de"
)
```

### 批量查询（无条件，默认前500条）

```python
skill.批量查询业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be"
)
```

### 批量查询（带条件）

```python
# 等值查询（默认 Operator=2）
skill.批量查询业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    filter_field="F0000002",
    filter_value="张三"
)

# 大于查询
skill.批量查询业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    filter_field="F0000003",
    filter_value="100",
    filter_operator=0  # 0=大于
)

# 分页查询（第101-200条）
skill.批量查询业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    from_row_num=100,
    to_row_num=200
)
```

**filter_operator 运算符对照：**

| 值 | 含义 |
|----|------|
| 0 | 大于 |
| 1 | 大于等于 |
| 2 | 等于（默认） |
| 3 | 小于等于 |
| 4 | 小于 |
| 5 | 不等于 |
| 6 | 在范围内 |
| 7 | 不在范围内 |

### 创建数据

```python
# 直接提交（默认）
skill.创建单条业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    data={
        "F0000002": "李四",
        "F0000003": "技术部"
    }
)

# 仅保存草稿
skill.创建单条业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    data={
        "F0000002": "李四",
        "F0000003": "技术部"
    },
    is_submit=False
)
```

### 更新数据

```python
skill.更新业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    biz_object_id="09a980d8-3b80-4f08-bbbd-732e0afa40de",
    data={
        "F0000003": "市场部"
    }
)
```

### 删除数据

```python
skill.删除业务数据(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    biz_object_id="09a980d8-3b80-4f08-bbbd-732e0afa40de"
)
```

### 上传附件

```python
skill.上传附件(
    schema_code="D28776428eaf3e1786c45e080e51e65573b69be",
    biz_object_id="09a980d8-3b80-4f08-bbbd-732e0afa40de",
    field_name="F0000011",  # 附件字段的字段编码，不是字段标题
    file_path="D:\\docs\\test.pdf"
)
```

### 下载附件

```python
skill.下载附件(
    attachment_id="fa5a96d4-559c-46c0-9dcc-dcb6e427a94c",  # 附件ID，不是URL
    output_path="D:\\download"  # 可选，默认保存到 ./download/
)
```

## 常见问题

**Q: 字段编码和字段标题有什么区别？**
A: 字段标题是用户在界面上看到的文字（如"客户名称"），字段编码是内部标识（如 `F0000002`），API 使用的是字段编码。

**Q: 如何确定字段编码？**
A: 先用 `批量查询业务数据` 查询一条数据，返回的 JSON 键名就是字段编码。

**Q: 下载附件的 attachment_id 从哪里获取？**
A: 查询业务数据时，附件字段的值就是附件ID（格式如 `fa5a96d4-559c-46c0-9dcc-dcb6e427a94c`），不是 URL 链接。

**Q: 批量查询最多返回多少条？**
A: 官方限制最大500条。如需更多数据，使用 `from_row_num` 和 `to_row_num` 分页查询。

**Q: 创建数据时 is_submit=False 是什么意思？**
A: `is_submit=False` 表示仅保存为草稿，不触发审批流程；`is_submit=True`（默认）表示直接提交。

---

版本：v1.1.2
