# 错误处理指南

本文档说明 DTS 文档查询 skill 中的错误处理策略。

## 404 处理

### 场景

用户查询一个不存在的类，例如 `acApi.wrongclass`。

### 处理流程

1. **尝试请求**：`http_fetcher.py` 请求 `WrongClass.html`
2. **检测 404**：返回状态码 404
3. **提示用户**：显示友好的错误信息
4. **请求输入**：询问用户提供正确的文档 URL
5. **保存映射**：将用户输入保存到 `data/url_mappings.json`
6. **重新查询**：使用正确的 URL 重新请求

### 示例对话

```
用户: acApi.wrongclass 如何使用？

Claude: ⚠️ 未找到 WrongClass 的文档 (404)

请提供正确的文档 URL，例如：
https://sdk.freedo3d.com/doc/api/CorrectClass.html

或者输入类名：CorrectClass

用户: https://sdk.freedo3d.com/doc/api/RealClass.html

Claude: ✅ 已记录映射：WrongClass → RealClass
正在重新查询...
```

### URL 映射文件

`data/url_mappings.json` 格式：

```json
{
  "WrongClass": "https://sdk.freedo3d.com/doc/api/RealClass.html",
  "OldName": "https://sdk.freedo3d.com/doc/api/NewName.html"
}
```

## 网络错误

### 重试策略

`http_fetcher.py` 使用 `urllib3.Retry` 实现自动重试：

```python
retry = Retry(
    total=3,           # 最多重试 3 次
    backoff_factor=1    # 每次间隔 1 秒
)
```

### 超时处理

- 连接超时：30 秒
- 超时后返回错误，不无限等待

### 错误信息

```
❌ 网络请求失败

可能的原因：
1. 网络连接中断
2. DTS 文档服务器无响应
3. URL 格式错误

建议：
- 检查网络连接
- 稍后重试
- 手动访问：https://sdk.freedo3d.com/doc/api/
```

## 解析错误

### 场景

HTML 结构不符合预期，导致解析失败。

### 处理策略

1. **记录错误**：在 stderr 中输出详细错误信息
2. **返回部分结果**：尽可能返回已解析的数据
3. **提示用户**：建议用户手动查看文档

### 示例

```python
try:
    methods = extract_methods(soup)
except Exception as e:
    print(f"Warning: Failed to parse methods: {e}", file=sys.stderr)
    print("Returning partial results...", file=sys.stderr)
    methods = []
```

## 缓存错误

### 缓存文件损坏

如果缓存文件无法读取：

1. **删除损坏的缓存**
2. **重新下载**
3. **重新解析**

### 缓存过期

默认缓存 7 天，过期后自动重新下载。

可以通过修改 `cache_manager.py` 中的 `timedelta(days=7)` 调整。

## 用户输入错误

### 无效的类名

如果用户输入不包含有效的类名：

```
用户: "如何使用这个功能？"

Claude: ❓ 无法识别 API 路径

请提供完整的 API 调用，例如：
- acApi.marker.add
- acApi.box.create

或者描述您的需求，例如：
- "如何添加标注点"
- "创建一个盒子"
```

### 空输入

```
用户: "acApi." (不完整的输入)

Claude: ❓ API 路径不完整

请提供完整的类名和方法名，例如：
- acApi.marker.add
- acApi.box.clear
```

## 调试技巧

### 启用详细日志

在脚本中添加调试输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 手动测试脚本

```bash
# 测试 HTTP 请求
python scripts/http_fetcher.py "https://sdk.freedo3d.com/doc/api/Marker.html" test.html

# 测试 HTML 解析
python scripts/html_parser.py test.html

# 测试缓存
python scripts/cache_manager.py --check Marker
python scripts/cache_manager.py --list

# 测试链接提取
python scripts/link_extractor.py test.html
```

### 查看缓存文件

```bash
# 查看所有缓存
python scripts/cache_manager.py --list

# 查看特定类的缓存
cat data/parsed/Marker.json

# 清理缓存
python scripts/cache_manager.py --clear
```
