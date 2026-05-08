---
name: cleanup-debug-scripts
overview: 清理 frontend-design 目录中 8 个无用的调试脚本
todos:
  - id: delete-debug-scripts
    content: 删除 8 个 debug_*.py 调试脚本
    status: completed
---

## 用户需求

检查并清理 `D:\MFAAvalonia-v2.12.0-win-x64\frontend-design` 目录中的无用 Python 脚本。

## 分析结果

目录中有 8 个 `debug_*.py` 调试脚本，均为开发 `generate_report.py` 过程中的一次性探索/调试脚本，其功能已完全整合进最终的 `generate_report.py`，无任何其他脚本依赖它们。

## 清理目标

删除以下 8 个文件：

- `debug_img.py` — 截图与日志节点匹配测试
- `debug_marker.py` — session 标记查找和节点统计
- `debug_match.py` — 节点名与截图匹配验证
- `debug_nodes.py` — 按行号范围提取节点
- `debug_parse.py` — 节点和截图关联解析
- `debug_parse2.py` — 另一种解析方式测试
- `debug_screenshot.py` — 截图时间戳匹配测试
- `debug_tasks.py` — Tasker.Task.Starting 查找

## 保留文件

- `generate_report.py`（主报告生成器）
- `agent_report.py`（Agent 监控脚本）
- `init_log.py`（初始化脚本）
- `maa-report.html`（生成的报告输出）