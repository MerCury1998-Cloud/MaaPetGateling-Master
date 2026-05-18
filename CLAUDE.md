# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

MaaPetGateling-Master 是一个基于 [MaaFramework](https://github.com/MaaXYZ/MaaFramework) 的游戏自动化项目，模板来自 [MaaPracticeBoilerplate](https://github.com/MaaXYZ/MaaPracticeBoilerplate)。通过图像识别技术实现游戏黑盒自动化测试。

## 目录结构

```
assets/
├── resource/          # 官服资源（中文）
│   ├── image/       # 模板图片 (.png)
│   ├── model/       # OCR 模型 (det.onnx, keys.txt, rec.onnx)
│   └── pipeline/    # 任务流水线 JSON (guild_hall.json, guild_boss.json 等)
├── resource_vin/     # 越南服资源
│   ├── image/
│   ├── model/
│   └── pipeline/    # guild_daily.json, daily_reward.json 等
├── config/           # maa_pi_config.json
└── interface.json   # MAA 接口配置（定义 controller、resource、task 入口）

agent/
├── main.py           # Agent 服务入口
├── my_action.py     # 自定义 Action 示例
└── my_reco.py        # 自定义 Recognition 示例

deps/tools/
├── pipeline.schema.json      # Pipeline JSON Schema（开发 pipeline 时参考）
├── custom.action.schema.json  # 自定义 Action Schema
└── custom.recognition.schema.json

tools/
├── configure.py      # 下载并配置 OCR 模型
├── install.py       # 安装依赖
├── validate_schema.py # 校验 JSON Schema
└── requirements.txt
```

## 开发命令

```bash
# 安装 Python 依赖
pip install -r tools/requirements.txt

# 配置 OCR 模型（下载到 assets/resource/model/ocr/）
python tools/configure.py

# 校验 pipeline JSON Schema
python tools/validate_schema.py

# 启动 Agent 服务
python agent/main.py <socket_id>
```

## 核心概念

### Pipeline（任务流水线）

每个 `.json` 文件（如 `guild_daily.json`）定义一组任务节点，格式为 `"节点名": { recognition, action, next, on_error, ... }`。

关键字段：
- `recognition`: 识别算法（`DirectHit`、`TemplateMatch`、`OCR` 等）
- `action`: 执行动作（`Click`、`Swipe`、`InputText`、`DoNothing`、`Command` 等）
- `next`: 成功后跳转的节点列表（按顺序匹配第一个识别到的）
- `on_error`: 识别超时或失败时的 fallback 节点列表（只引用其他已定义的节点名，不支持内联对象）
- `timeout`: 识别超时（毫秒），默认 20000
- `target`: `true` 表示识别到才执行 action
- `repeat`: 重复次数

### interface.json

定义可用的 Controller（ADB/Win32）、Resource（资源路径）、Task（入口任务名）。修改 task 入口对应修改此文件。

### 模板图片命名

模板匹配优先用 `任务名.png`，如 `公会图标.png`、`返回.png`。越南服模板在 `resource_vin/image/` 下。

## 注意事项

- Pipeline JSON 中的 `on_error` 必须是**已定义的节点名字符串数组**，不是内联对象
- `Click_top3` 等节点在多个 pipeline 文件中**不能同名**，加载时会冲突
- 不同服的资源互相独立：`resource/` 是官服，`resource_vin/` 是越南服
- OCR 模型不在仓库中，需要运行 `python tools/configure.py` 下载
- 新增 pipeline 文件后，确认 `interface.json` 的 `resource` 中已包含对应路径
