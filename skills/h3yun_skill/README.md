# 氚云 (H3Yun) OpenClaw Skill

## 功能说明

该 Skill 提供了与氚云平台集成的能力，支持：

| 功能 | 说明 |
|------|------|
| 查询单条业务数据 | 根据 SchemaCode 和 BizObjectId 查询单条数据 |
| 批量查询业务数据 | 支持按条件过滤、分页查询 |
| 创建单条业务数据 | 新增一条业务数据 |
| 更新业务数据 | 更新指定 ID 的业务数据 |
| 删除业务数据 | 删除指定 ID 的业务数据 |
| 上传附件 | 上传文件到氚云表单的附件字段 |
| 下载附件 | 从氚云下载附件到本地 |

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

## 表单编号和字段名如何确定

### 1. 获取表单编码 (SchemaCode)

1. 登录氚云管理后台
2. 进入 **应用管理** → 选择你的应用
3. 找到需要操作的表单，点击 **设置**
4. 在表单设置页面可以看到 **表单编码 (SchemaCode)**

### 2. 获取字段名称

**方式 1：在表单设计器中查看**
1. 进入表单设计器
2. 选中任意字段
3. 在右侧属性面板查看 **字段名称**（不是字段标题！）

**方式 2：通过 API 查询（推荐）**
先用 `查询单条业务数据` 或 `批量查询业务数据` 查询一条数据，返回的 JSON 键名就是字段名称：

```json
{
  "BizObjectId": "xxx",
  "字段名称1": "值1",
  "字段名称2": "值2"
}
```

## 使用示例

### 查询单条数据

```python
skill.查询单条业务数据(
    schema_code="你的SchemaCode",
    biz_object_id="业务对象ID"
)
```

### 批量查询

```python
skill.批量查询业务数据(
    schema_code="你的SchemaCode",
    filter_field="姓名",
    filter_value="张三",
    page_index=1,
    page_size=20
)
```

### 创建数据

```python
skill.创建单条业务数据(
    schema_code="你的SchemaCode",
    data={
        "姓名": "李四",
        "年龄": 30,
        "部门": "技术部"
    }
)
```

### 更新数据

```python
skill.更新业务数据(
    schema_code="你的SchemaCode",
    biz_object_id="业务对象ID",
    data={
        "年龄": 31
    }
)
```

### 删除数据

```python
skill.删除业务数据(
    schema_code="你的SchemaCode",
    biz_object_id="业务对象ID"
)
```

### 上传附件

```python
skill.上传附件(
    schema_code="你的SchemaCode",
    biz_object_id="业务对象ID",
    field_name="附件字段名",
    file_path="D:\\test.pdf"
)
```

### 下载附件

```python
skill.下载附件(
    attachment_url="https://...",
    output_path="D:\\downloaded.pdf"
)
```

## 常见问题

**Q: 字段名称和字段标题有什么区别？**
A: 字段标题是用户在界面上看到的文字（如"客户名称"），字段名称是内部标识（如"CustomerName"），API 使用的是字段名称。

**Q: 如何确定字段类型？**
A: 查询一条数据，看返回值的类型：
- 字符串：`"abc"`
- 数字：`123`
- 日期：`"2024-01-01"`
- 选项：`"选项值"`

**Q: 附件字段如何填写？**
A: 上传时需要提供：
- `field_name`: 附件字段的字段名称
- `file_path`: 本地文件的完整路径

---

版本：v1.0.0
