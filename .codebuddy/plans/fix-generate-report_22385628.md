---
name: fix-generate-report
overview: 重写 generate_report.py，采用"截图优先"策略，将 vision 目录截图与 maafw.log 一一对应，生成正确的测试报告
todos:
  - id: rewrite-parse
    content: 重写 parse_log_for_execution 为截图优先+日志补充的解析逻辑
    status: completed
  - id: fix-html-gen
    content: 修复 HTML 生成：base64嵌入截图、正确显示节点名和识别信息
    status: completed
    dependencies:
      - rewrite-parse
  - id: test-verify
    content: 运行脚本验证报告正确性
    status: completed
    dependencies:
      - fix-html-gen
---

## 产品概述

重写 MAA 执行报告生成脚本，将 `debug/vision/` 目录中的截图与 `debug/maafw.log` 日志一一对应，生成完整的自动化测试报告。

## 核心需求

- 扫描 vision 目录中的截图，解析文件名获取时间戳、节点名、reco_id
- 按 reco_id 在日志中匹配对应的 `Node.PipelineNode.Succeeded` 行，提取识别算法、OCR文本、置信度、点击坐标等
- 截图以 base64 嵌入 HTML，避免浏览器 file:/// 协议安全限制
- 按执行轮次分组（时间间隔>30秒视为新一轮），默认展示最新一轮
- 过滤掉 InitLog/GenerateReport 等非业务节点
- 每个节点卡片展示：截图 + 节点名 + 时间 + 识别算法 + OCR文本 + 置信度 + 点击坐标

## 技术栈

- Python 3（标准库：re, os, json, base64, datetime, pathlib）
- HTML + CSS（内联在 Python 脚本中生成）

## 实现方案

### 根因分析

当前脚本有3个致命问题：

1. **Session标记定位错误**：脚本找到最新的 `===REPORT_SESSION_START===`（日志第2058行），该标记由 GenerateReport_WriteMarker 写入，之后只有3个 GenerateReport 节点，没有业务节点。业务节点在标记之前的第1-2057行。

2. **节点名称提取错误**：`Node.PipelineNode.Succeeded` 的 JSON 中，顶层 `"name"` 是父节点名（如 "InitLog_End"），不是当前执行节点名。真实节点名在 `node_details.name` 中（如 "Guild_Enter"）。

3. **截图不显示**：session标记后的 reco_id（400000238-400000240）在 vision 目录中无对应截图；且 `file:///` 协议在浏览器中有安全限制。

### 核心策略：截图优先 + 日志补充

不再依赖 session 标记，改为以截图为主数据源，日志为补充信息源：

1. **扫描 vision 目录**：获取所有截图，解析文件名得到 (timestamp, node_name, reco_id)
2. **分组运行轮次**：按时间戳间隔分组（>60秒无截图=新轮次），选择最新一轮
3. **匹配日志**：对每个截图的 reco_id，在日志中搜索包含该 reco_id 的 `Node.PipelineNode.Succeeded` 行
4. **正确提取字段**：从 `node_details.name` 获取真实节点名，从 `reco_details` 获取算法/分数/OCR文本，从 `action_details` 获取点击坐标
5. **截图嵌入为 base64**：将截图转为 base64 嵌入 HTML，彻底解决 file:/// 协议问题
6. **过滤非业务节点**：排除 InitLog_/GenerateReport_ 等辅助节点

### 数据流

```
vision/*.jpg ──解析文件名──> [(timestamp, node_name, reco_id, path), ...]
                                         │
                                         ▼
                              按时间间隔分组 → 选最新轮次
                                         │
maafw.log ──搜索reco_id──> 匹配 Node.PipelineNode.Succeeded
                                         │
                                         ▼
                          提取: node_details.name, reco_details, action_details
                                         │
                                         ▼
                              合并为节点列表 → 生成 HTML（截图base64嵌入）
```

### 目录结构

```
D:\MFAAvalonia-v2.12.0-win-x64\frontend-design\
└── generate_report.py  # [MODIFY] 重写整个脚本
```

### 实现要点

1. **截图文件名解析**：格式 `2026.05.08-15.37.04.908_Guild_Enter_400000134.jpg`，用正则 `r'(\d{4}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}\.\d{3})_(.+)_(\d+)\.jpg'` 提取三部分

2. **轮次分组算法**：将截图按时间排序，相邻截图时间差>60秒则视为新一轮。取最新一轮生成报告

3. **日志匹配**：对 reco_id 搜索 `f'"reco_id":{reco_id}'` 在 `Node.PipelineNode.Succeeded` 行中，然后用正则从 `node_details` 和 `reco_details` 子对象提取信息

4. **base64嵌入**：读取截图文件，`base64.b64encode()` 后以 `data:image/jpeg;base64,{data}` 格式嵌入img src，彻底避免文件协议问题

5. **性能考虑**：截图可能有40-50张，base64嵌入会使HTML较大（约30-50MB），但可确保跨浏览器兼容。可考虑添加压缩/缩略图选项

6. **TemplateMatch细节**：TemplateMatch 节点的 detail 中没有 text 字段，只有 score 和 box，需特殊处理