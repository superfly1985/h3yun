# 氚云项目文件放置规则

> 版本：v1.0.0
> 更新日期：2026-04-10

## 目录结构规范

```
01.氚云读写方法/
├── src/              # 核心源代码
├── data/             # 数据操作脚本（独立可执行）
├── test/             # 测试文件和临时脚本
├── config/           # 配置文件（JSON格式）
├── document/         # 文档说明
├── demo/             # 演示示例
├── download/         # 下载文件存放
├── image/            # 图片资源
├── plan/             # 开发计划
├── assets/           # 静态资源
├── i18n/             # 国际化文件
├── .trae/rules/      # 项目规则
└── changelog.md      # 变更日志
```

---

## 文件放置规则

### 1. src/ - 核心源代码
**放置内容：**
- 核心类定义（H3YunClient、H3YunConfig）
- CLI入口（cli.py）
- 可复用的工具函数

**禁止放置：**
- 测试脚本
- 临时脚本
- 配置文件
- 演示代码

**示例：**
```
src/
├── __init__.py
├── h3yun_client.py      # HTTP客户端
├── h3yun_config.py      # 配置管理
└── cli.py               # 命令行入口
```

---

### 2. data/ - 数据操作脚本
**放置内容：**
- 独立可执行的数据操作脚本
- 单功能脚本（读取、新增、更新、删除、上传、下载）

**特点：**
- 每个脚本独立运行
- 通过命令行参数接收输入
- 不依赖其他脚本

**示例：**
```
data/
├── LoadBizObject.py        # 单条读取
├── LoadBizObjects.py       # 批量读取
├── CreateBizObject.py      # 单条新增
├── CreateBizObjects.py     # 批量新增
├── UpdateBizObject.py      # 单条更新
├── RemoveBizObject.py      # 删除
├── UploadAttachment.py     # 上传附件
└── DownloadBizObjectFile.py # 下载附件
```

---

### 3. test/ - 测试和临时脚本
**放置内容：**
- 单元测试脚本
- 临时测试脚本（用一次即弃）
- 测试数据文件（JSON、txt）
- 环境配置示例（.env.example）

**命名规范：**
- 测试脚本：`test_*.py`
- 临时脚本：`tmp_*.py` 或 `verify_*.py`
- 数据文件：`*_example.json`、`*_submit.json`

**示例：**
```
test/
├── test_cli_read_write.py      # 单元测试
├── h3yun.env.example           # 环境配置示例
├── target_biz_id.txt           # 测试数据
├── update_biz.json             # 更新测试数据
├── matcher_submit.json         # 匹配器测试数据
└── tmp_verify_matcher.py       # 临时验证脚本（用完删除）
```

**重要：** 临时脚本使用后应及时删除，保持目录整洁。

---

### 4. config/ - 配置文件
**放置内容：**
- JSON格式的业务配置文件
- 上传配置、下载配置、过滤配置

**格式要求：**
- 必须使用JSON格式
- 文件名使用小写，单词间用点分隔

**示例：**
```
config/
├── upload.pic.json         # 上传图片配置
├── download.pic.json       # 下载图片配置
└── filter.pic.json         # 过滤条件配置
```

---

### 5. document/ - 文档
**放置内容：**
- 接口说明文档
- 使用指南
- 环境要求
- 操作经验

**格式：**
- Markdown格式（.md）

**示例：**
```
document/
├── 接口说明.md
├── 导出说明.md
├── 操作经验.md
├── 环境要求.md
└── 目录说明.md
```

---

### 6. demo/ - 演示示例
**放置内容：**
- 可运行的演示脚本
- 用法示例
- 最佳实践展示

---

### 7. download/ - 下载文件
**放置内容：**
- 程序下载的文件
- 临时下载目录

**注意：**
- 此目录内容不提交到版本控制
- 已在 .gitignore 中排除

---

### 8. image/ - 图片资源
**放置内容：**
- 文档配图
- 截图
- 示例图片

**子目录：**
```
image/
└── changelog/          # changelog配图
```

---

### 9. plan/ - 开发计划
**放置内容：**
- 开发计划文档
- 需求文档
- 迭代规划

---

## 禁止放置的文件类型

| 文件类型 | 禁止放置位置 | 正确位置 |
|----------|--------------|----------|
| 测试脚本 | src/、data/ | test/ |
| 临时脚本 | src/、data/、根目录 | test/（用完删除） |
| 配置文件 | src/、根目录 | config/ |
| 演示代码 | src/、data/ | demo/ |
| 下载文件 | src/、data/、根目录 | download/ |

---

## 新增文件检查清单

在创建新文件前，请确认：

- [ ] 文件类型与目标目录匹配
- [ ] 文件名符合命名规范
- [ ] 临时脚本已标记（tmp_前缀）
- [ ] 测试数据已放入 test/
- [ ] 配置文件已放入 config/

---

## 规则更新

如需更新此规则文件：
1. 修改 `.trae/rules/project_rules.md`
2. 更新版本号（遵循 SemVer）
3. 更新更新日期
4. 在 changelog.md 中记录变更
