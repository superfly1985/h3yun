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
