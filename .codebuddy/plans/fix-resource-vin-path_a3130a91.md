---
name: fix-resource-vin-path
overview: 修改 interface.json 中"外网越南文版"的 path 配置，让它先加载基础 resource 再叠加 resource_vin。
todos:
  - id: fix-resource-path
    content: 修改 assets/interface.json 中"外网越南文版"的 path 为 ["./resource", "./resource_vin"]
    status: completed
---

修改 interface.json 中"外网越南文版"的资源路径，使其先加载基础资源 `./resource`，再叠加加载 `./resource_vin`，实现资源继承覆盖，让越南文版能正确使用基础 pipeline 和图片资源。

## 核心修改

- 将"外网越南文版"的 `path` 从 `["./resource_vin"]` 改为 `["./resource", "./resource_vin"]`
- 与官方 MAA 示例中 Bilibili 资源包的写法保持一致
- 不添加 mirrorchyan_rid 字段

## 修改方案

修改文件 `assets/interface.json` 第 40-45 行，将"外网越南文版"的 path 数组从单路径改为双路径，遵循官方 MAA 的 ProjectInterface V2 协议中资源覆盖规则。

### 修改内容

```
{
    "name": "外网越南文版",
    "path": [
-       "./resource_vin"
+       "./resource",
+       "./resource_vin"
    ]
}
```

### 原理

根据 PI V2 协议文档（3.3-ProjectInterfaceV2协议.md）第 218-221 行：

> `path` 加载的路径数组。如果提供多个路径，会依次加载，后加载的资源会覆盖前加载的资源。

即先加载 `./resource`（基础中文版全部内容），再加载 `./resource_vin`（越南文覆盖内容），同名任务/图片会被覆盖，其余保持不变。