## v1.1.4（发布日期：2026-04-20）

### 🐛 Bug 修复：添加 SKILL.md 规范

根据用户反馈添加 SKILL.md 文件，符合 OpenClaw AgentSkills 规范。

### 修复内容
- 🐛 **创建 SKILL.md 文件**（规范要求）
  - 添加 YAML frontmatter（name + description）
  - description 包含触发关键词：氚云、H3Yun、业务数据、表单操作、查询表单、创建数据、更新记录、删除数据、上传附件、下载附件
  - 简洁的指令风格 body，包含配置、字段说明、Actions
- 🐛 **删除 README.md**（规范要求）
  - 按规范只保留 SKILL.md，删除面向用户的 README.md

## v1.1.3（发布日期：2026-04-19）

### 🐛 Bug 修复：Skill 返回值结构优化

根据用户反馈优化 Skill 返回值结构，使其更符合使用直觉。

### 修复内容
- 🐛 **下载附件参数名使用关键字参数**（问题2）
  - 修复前：`self.client.download_attachment(attachment_id, output_path)` 使用位置参数
  - 修复后：`self.client.download_attachment(attachment_id, out_dir=output_path)` 使用关键字参数
- 🐛 **查询单条返回提取后的业务数据**（问题4）
  - 修复前：返回完整 API 响应 `{"ReturnData": {"BizObject": {...}}}`
  - 修复后：直接返回 `BizObject` 内容，用户无需再嵌套提取
- 🐛 **批量查询返回简化结构**（问题4）
  - 修复前：返回完整 API 响应
  - 修复后：返回 `{"BizObjectArray": [...], "TotalCount": N}`，更直观
- 🐛 **创建/更新/删除/上传附件返回简化结构**（问题4）
  - 统一提取关键字段（BizObjectId、AttachmentId 等），减少嵌套层级
- 🐛 **文档说明字段命名的三种类型**（问题5）
  - 修复前：仅说明 F0000002 格式的"字段编码"
  - 修复后：说明固有字段（ObjectId/Name）、自动字段（F0000002）、自定义字段（UserName）三种类型，强调以实际查询为准
- 🐛 **skill.py 添加版本常量**（问题6）
  - 新增 `__version__ = "1.1.3"` 和 `H3YunSkill.VERSION` 类属性

## v1.1.2（发布日期：2026-04-16）

### 🐛 Bug 修复：Skill 歧义与不一致

修复 OpenClaw Skill 中多处可能导致用户误用的歧义描述和接口不一致问题。

### 修复内容
- 🐛 **manifest.json 批量查询参数与 skill.py 不一致**（P0 严重）
  - 修复前：manifest 使用 `page_index`/`page_size`（页码/每页数量），代码实际使用 `from_row_num`/`to_row_num`（行号）
  - 修复后：manifest 参数与代码对齐，使用 `from_row_num`/`to_row_num`，并补充说明分页规则
- 🐛 **下载附件参数名误导**（P0 严重）
  - 修复前：参数名 `attachment_url` 暗示传 URL 链接，实际需要附件ID
  - 修复后：参数名改为 `attachment_id`，描述明确标注"不是URL，是附件的唯一标识ID"
- 🐛 **README 示例与代码不一致**（P1 重要）
  - 修复前：示例使用 `page_index`/`page_size`、中文字段名
  - 修复后：示例使用 `from_row_num`/`to_row_num`、字段编码（如 `F0000002`）
- 🐛 **字段名说明缺失**（P1 重要）
  - 修复前：未说明 API 使用字段编码而非字段标题
  - 修复后：新增"字段编码 vs 字段标题"章节，提供获取字段编码的方法
- 🐛 **manifest.json 版本号过时**（P2）
  - 修复前：`version: "1.0.0"`
  - 修复后：`version: "1.1.2"`
- 🐛 **创建数据无法选择是否提交**（P2）
  - 修复前：`创建单条业务数据` 无 `is_submit` 参数，默认直接提交
  - 修复后：新增 `is_submit` 参数，默认 `True`（提交），可设为 `False`（保存草稿）
- 🐛 **上传附件 field_name 描述不清**（P2）
  - 修复前：描述为"附件字段名称"
  - 修复后：描述为"附件字段的字段编码（如 F0000011），不是字段标题"
- 🐛 **过滤条件只支持等值查询**（P3）
  - 修复前：硬编码 `Operator: 2`（等于），无法做其他比较
  - 修复后：新增 `filter_operator` 参数，支持 0-7 共8种运算符

## v1.1.1（发布日期：2026-04-14）

### 🐛 Bug 修复：与官方 API 一致性

修复 SDK 与氚云官方 API 文档不一致的问题。

### 修复内容
- 🐛 **LoadBizObjects Filter 结构错误**（P0 严重）
  - 修复前：Filter 参数需用户自行拼 JSON，且缺少 `FromRowNum`、`ToRowNum`、`RequireCount`、`ReturnItems`、`SortByCollection` 等必要字段
  - 修复后：新增 `build_filter()` 静态方法，按官方规范构建完整 Filter 结构
  - 修复后：`load_biz_objects()` 方法支持 `from_row_num`、`to_row_num`、`matcher`、`return_items` 参数，自动构建 Filter
  - 修复后：Matcher 结构使用官方规范的 `Matchers` 字段（原 `ChildItems` 已修正）
  - 官方文档：https://help.h3yun.com/contents/1007/1633.html
- 🐛 **DownloadBizObjectFile Content-Type 缺失**（P3）
  - 修复前：下载附件请求未显式设置 Content-Type
  - 修复后：显式设置 `Content-Type: application/x-www-form-urlencoded`
  - 官方文档：https://help.h3yun.com/contents/1013/1639.html
- 📝 **README 批量查询示例错误**
  - 修复前：示例中 Filter 结构不完整，缺少必要字段
  - 修复后：更新为使用 `build_filter()` 和 `load_biz_objects()` 新 API

### API 变更
- `load_biz_objects(schema_code, params)` → `load_biz_objects(schema_code, filter_str=None, from_row_num=0, to_row_num=500, matcher=None, return_items=None)`
- 新增 `H3YunClient.build_filter()` 静态方法

---

## v1.1.0（发布日期：2026-04-14）

### ✨ 新增功能：OpenClaw Skill 支持

新增 OpenClaw Skill 模块，可直接在 OpenClaw 中作为技能使用。

### 主要特性
- ✅ 新增 `skills/h3yun_skill/` - 完整的 OpenClaw Skill
- ✅ Skill 支持 OpenClaw 配置 + 环境变量双重配置
- ✅ 完全独立的 Skill 文件夹，可直接分发
- ✅ 7个可用功能（增删改查+附件）
- ✅ 完整的 manifest.json 配置文件
- ✅ 无硬编码敏感信息，运行时由用户配置

### Skill 结构
```
h3yun_skill/
├── h3yun/              # SDK核心代码
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   └── exceptions.py
├── skill.py            # Skill入口
├── manifest.json     # Skill配置
├── requirements.txt   # 依赖
└── README.md        # 使用说明
```

---

## v1.0.0（发布日期：2026-04-10）

### 🎉 正式发布

首个稳定版本，可用于生产环境。

### 主要特性
- ✅ 完整的业务数据 CRUD 操作（增删改查）
- ✅ 附件上传/下载支持
- ✅ 批量操作自动分批处理
- ✅ 自动重试机制（指数退避）
- ✅ 完整的类型提示和文档
- ✅ 6种自定义异常类
- ✅ 配置验证机制
- ✅ 日志系统支持
- ✅ 内部私有库（Git安装）

### 项目结构
- 标准包结构 `src/h3yun/`
- 8个使用示例 `examples/`
- 完善的 `.gitignore` 防止敏感信息泄露

---

## v0.1.0（发布日期：2026-04-10）
### 重大重构
- 重构：src/ 改为标准包结构 `src/h3yun/`
- 新增：自定义异常类模块 `exceptions.py`
- 新增：完整的类型提示和文档字符串
- 新增：自动重试机制（urllib3）
- 新增：配置验证功能
- 新增：日志系统支持
- 新增：批量操作自动分批处理
- 重构：data/ 目录改为 examples/，脚本改为使用示例
- 新增：setup.py 准备 PyPI 发布

### 删除和清理
- 删除：H3yunTool.py（硬编码导入路径）
- 删除：h3yun.config.json、.h3yun.quick.json
- 删除：assets/.gitkeep、demo/.gitkeep、plan/.gitkeep
- 删除：i18n/ 空目录
- 删除：test/target_biz_id.txt

## v0.0.8-dev（发布日期：2026-04-10）
- 修复：移除所有硬编码的 `Web_Service/氚云/` 路径引用
- 修复：data/ 目录下7个文件的导入路径统一改为 `from src.xxx`
- 修复：cli.py 环境文件搜索路径改为 `test/.env` 和 `test/h3yun.env`
- 修复：h3yun_client.py 默认下载目录改为 `./download`

## v0.0.7-dev（发布日期：2026-04-10）
- 修复：LoadBizObjects 的 Matcher 结构改为官方规范格式（`Type: Item, Name, Operator, Value`），原 `Type: Equal, Left, Right` 格式会导致过滤条件不生效
- 修复：同步更新 data/LoadBizObjects.py、config/filter.pic.json、H3yunTool.py 中的 Matcher 结构

## v0.0.6-dev（发布日期：2025-12-05）
- 优化：UpdateBizObject 支持 `--biz-file`，新增 PowerShell 脚本 `update-one.ps1`

## v0.0.5-dev（发布日期：2025-12-05）
- 新增：UpdateBizObject 单条更新支持，CLI `update-one`
- 优化：CLI 支持 `--env-file`、`--matcher-file`、`--timeout`；新增脚本避免REPL/转义问题

## v0.0.4-dev（发布日期：2025-12-05）
- 修正：批量新增默认改为提交状态（IsSubmit=true），CLI默认提交

## v0.0.3-dev（发布日期：2025-12-05）
- 新增：批量新增 CreateBizObjects 支持，CLI `create-many`
- 文档：补充批量新增章节

## v0.0.2-dev（发布日期：2025-12-05）
- 新增：CreateBizObject 单条新增支持，CLI `create-one`
- 文档：补充接口说明的新增章节

## v0.0.1-dev（发布日期：2025-12-05）
- 新增：单条读取 LoadBizObject 成功，新增 CLI `load-one`
- 新增：批量读取 LoadBizObjects 支持，新增 CLI `load-many` 与 Filter 构建

## v0.0.0-dev（初始化日期：2025-12-05）
- 初始化目录结构：src、test、document、demo、i18n、assets、plan
