---
name: dts-docs-query
description: |
  查询 DTS SDK API 文档的智能助手。

  支持功能：
  1. 精确查询：解析 acApi.module.method 格式的 API 调用，返回详细文档
  2. 自然语言查询：理解"如何添加标注点"等自然语言问题
  3. 惰性爬取：按需从 https://sdk.freedo3d.com/doc/api/ 获取文档
  4. 本地缓存：自动缓存已查询的 API，节省 token 和时间

  触发关键词：DTS、孪生、地图、acApi、freedo
---

本文档引用了 plugin 中的实际实现。以下指令定义在：
`../../skills/dts-docs-query/query.py`

当用户询问 DTS SDK API 时，按以下流程处理：

## 1. 识别查询类型

**精确查询**：用户明确指定 API 路径
```
acApi.marker.add -> 查询 Marker.add 方法
```

**自然语言查询**：用户描述需求
```
"如何添加标注点" -> 搜索相关 API（Marker.add）
```

## 2. 执行查询

使用以下脚本：
```bash
python skills/dts-docs-query/query.py "$ARGUMENTS"
```

## 3. 参考文档

详细实现说明见：
- [API 结构说明](../../skills/dts-docs-query/references/dts-api-structure.md)
- [错误处理指南](../../skills/dts-docs-query/references/error-handling.md)
- [完整实现](../../skills/dts-docs-query/SKILL.md)
