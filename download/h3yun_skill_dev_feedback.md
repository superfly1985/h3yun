# SKILL.md 编写规范（反馈给开发者）

> 整理时间：2026-04-20
> 基于 OpenClaw AgentSkills 规范

---

## 1. 必须有 YAML frontmatter（SKILL.md 顶部）

```yaml
---
name: skill名称（小写，横线分隔）
description: 技能描述，说明何时触发本技能（这是主要触发机制）
---
```

**description 写法要点：**
- 技能做什么
- **何时应该触发**（用户说了什么话时激活）
- 具体触发关键词

**反面例子：**
```yaml
description: 氚云平台API操作技能
```

**正面例子：**
```yaml
description: 读写氚云 (H3Yun) 平台的业务数据，支持增删改查、附件上传下载。当用户提到氚云、H3Yun、业务数据、表单操作时触发。
```

---

## 2. 目录结构规范

```
skill-name/
├── SKILL.md          ← 必须有这个文件
├── manifest.json     ← 技能注册配置（可选保留）
├── scripts/          ← 可选：可执行脚本
├── references/       ← 可选：参考文档
└── assets/           ← 可选：资源文件
```

**禁止包含的文件（不要有）：**
- README.md
- INSTALLATION_GUIDE.md
- CHANGELOG.md
- 等辅助文档

> 技能目录只放 AI Agent 执行任务时真正需要的文件，不需要面向用户的文档。

---

## 3. SKILL.md body 内容规范

- 用指令风格写，简洁优先
- 示例要正确（参数名与 SDK 一致）
- 返回值结构需要说明
- 过长内容放 `references/` 目录，SKILL.md 只做索引和关键示例

**body 不需要的内容：**
- "何时使用本技能"章节（description 已经说明了）
- 安装指南、变更日志等辅助内容

---

## 4. 当前 h3yun skill 需要修复的具体问题

### P2：查询单条返回值未说明嵌套结构

SKILL.md 应说明 `load_biz_object` 返回结构为：
```json
{
  "success": true,
  "data": {
    "Successful": true,
    "ReturnData": {
      "BizObject": {
        "ObjectId": "xxx",
        "字段名": "值"
      }
    }
  }
}
```

调用方需要按层级访问：`data.ReturnData.BizObject.字段名`

### P2：字段编码说明需补充

当前只说"F 开头格式（如 F0000002）"，但实际上：
- 有些表单用 F 开头（如 F0000002）
- 有些表单用自然名称（如 UserName、Password）

**应在 SKILL.md 中说明：以批量查询返回的 JSON 键名为准，F 格式和非 F 格式均可能出现。**

### P3：版本号一致性

建议在 `skill.py` 顶部加一行：
```python
__version__ = "1.1.2"
```

并与 `manifest.json` 保持同步。

---

## 5. 文件命名

- skill 目录名 = name 字段值
- 全小写，用横线分隔
- 示例：`h3yun` / `feishu-doc` / `document-retriever`

---

## 参考：其他 skill 的 SKILL.md 结构

### ai-ppt-generate
```yaml
---
name: ai-ppt-generate
description: Generate PowerPoint presentations using Baidu AI PPT API. Use when user asks to create a PPT, make slides, generate a presentation, or create slides from a topic/outline. Triggers on phrases like "create a PPT", "生成PPT", "制作幻灯片", "make a presentation".
---

# AI PPT Generate

## Scripts
...

## Usage Examples
...
```

### feishu-doc
```yaml
---
name: feishu-doc
description: |
  Feishu document read/write operations. Activate when user mentions Feishu docs, cloud docs, or docx links.
---

# Feishu Document Tool

## Token Extraction
...

## Actions
...
```
