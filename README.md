# H3yunTool 使用说明（English + 中文）

## 概述
- H3yunTool 是一个面向氚云 OpenAPI 的通用数据管理 GUI 工具，支持查询、编辑、删除以及附件上传/下载。
- 目标：作为独立程序包复用，减少配置和操作复杂度。

## 目录与配置
- 位置：`Web_Service/氚云/H3yunTool.py`
- 环境认证：`Web_Service/氚云/.env`（仅需 `H3YUN_ENGINE_CODE`、`H3YUN_SECRET`）
- 应用配置：`Web_Service/氚云/h3yun.config.json`（自动加载与自动保存，示例）

```json
{
  "schema": "D287764relabel",
  "id": "<BizObjectId>",
  "attach_field": "pic",
  "full_details": true,
  "search": { "field": "ObjectId", "value": "<BizObjectId>" },
  "edit": { "field": "IP", "value": "114.114.114.114" },
  "upload": { "dir": "Web_Service/氚云/image/changelog", "patterns": ["*.png","*.jpg"] },
  "download": { "out": "Web_Service/氚云/download/pic" }
}
```

## 启动
- `python Web_Service/氚云/H3yunTool.py`
- 自动加载 `h3yun.config.json`；界面变更自动保存（无弹窗）。

## 功能
- Load One 查询单条：输入 `Schema` 与 `BizObjectId`，显示完整字段列表
- Load Many 批量查询：可输入查询字段与值；可勾选“Full Details 全字段”以逐条补齐字段集合
- Update 更新：点击表格字段或表头自动填入编辑字段与值，点击“更新”提交
- Remove 删除：按当前 `BizObjectId` 删除
- Create 新增：弹窗列出当前表格列（排除系统字段），为每列提供输入框，提交后自动读取新记录
- Attach 附件：设置附件字段，选择文件或目录批量上传；支持下载到输出目录

## 交互优化
- 行选择：选中行自动将 `ObjectId` 填入 `BizObjectId`
- 字段选择：点击单元格或表头自动填入编辑字段（以及附件字段）与值
- 滚动条：列表带水平/垂直滚动条以适配宽表与长表

## 泛用性设计
- 动态字段：不假定 IP 或 pic 为固定字段；按实际返回列动态构建显示与新增窗口
- 可移植：仅依赖 `.env` 与 `h3yun.config.json` 两个文件；可通过 PyInstaller 等打包为独立程序

## 打包建议
- 进入项目根：`cd d:\OneDrive\01.project\35.Config_Search`
- 安装依赖：`pip install -r Web_Service/氚云/requirements.txt`
- 生成 exe（示例）：
  - `pyinstaller -F Web_Service/氚云/H3yunTool.py -n H3yunTool`
  - 将 `.env` 与 `h3yun.config.json` 放入与 exe 同目录即可运行

## 变更说明
- 清理未使用方法：移除旧的 `create_one/create_many` 辅助方法，统一用“Create 新增”弹窗实现
- 字段泛化：附件字段与优先显示列按返回结果动态生成，避免空值与不匹配
- 配置行为：启动自动加载；关键字段变更自动持久化；快速保存保留，无成功提示弹窗

## 常见问题
- 为什么批量查询不返回所有字段？
  - 批量接口按 `ReturnItems` 返回列，勾选“Full Details 全字段”后工具会逐条补齐字段集合
- 附件字段不是固定的？
  - 是的，附件字段由用户选择（点击列或手动输入），工具按当前设定进行上传与下载
