# JSDoc HTML 选择器指南

本文档说明如何从 DTS SDK 的 JSDoc 生成的 HTML 中提取信息。

## HTML 结构概述

DTS SDK 使用 Sunlight 文档生成器，生成的 HTML 结构如下：

```html
<div id="main">
  <h1 class="page-title">Class: Marker</h1>
  <div class="class-description">...</div>

  <!-- 方法列表 -->
  <h4 class="name" id="add">
    <span class="signature">(data, fn)</span>
  </h4>

  <!-- 方法描述 -->
  <div class="description">...</div>

  <!-- 参数表格 -->
  <table class="params table table-striped">
    <tr>
      <td class="name"><code>data</code></td>
      <td class="type"><span class="param-type">object</span></td>
      <td class="last">参数描述</td>
    </tr>
  </table>
</div>
```

## 关键 CSS 选择器

### 类名和描述

```python
# 类名
soup.find('h1', class_='page-title').text

# 提取 "Marker" 从 "Class: Marker"
class_name = soup.find('h1', class_='page-title').text.replace('Class: ', '')

# 类描述
soup.find('div', class_='class-description')
```

### 方法列表

```python
# 查找所有方法
methods = soup.find_all('h4', class_='name')

# 方法名
method_elem.get('id')  # 例如："add"

# 方法签名
method_elem.find('span', class_='signature').text  # 例如："(data, fn)"
```

### 方法描述

```python
# 找到方法后的 <dd> 元素
dd_element = method_elem.find_next('dd')

# 提取描述
description_elem = dd_element.find('div', class_='description')
description = description_elem.get_text(strip=True)
```

### 参数表格

```python
# 参数表格
params_table = dd_element.find('table', class_='params')

# 遍历参数
tbody = params_table.find('tbody')
for tr in tbody.find_all('tr'):
    name = tr.find('td', class_='name').text.strip()
    param_type = tr.find('td', class_='type').text.strip()
    desc = tr.find('td', class_='last').get_text(strip=True)
```

### 返回值

```python
# 查找 "Returns:" 标题
returns_elem = dd_element.find('h5', string='Returns:')

if returns_elem:
    returns_div = returns_elem.find_next('div')
    returns = returns_div.get_text(strip=True)
```

### 代码示例

```python
# 查找 "Example:" 标题
example_elem = dd_element.find('h5', string='Example:')

if example_elem:
    pre_elem = example_elem.find_next('pre')
    code_elem = pre_elem.find('code')
    example_code = code_elem.text
```

## 解析注意事项

1. **换行符和空格**：参数类型可能包含换行符（如 `object | array`），需要清理
2. **嵌套类型**：复杂参数类型可能包含多行描述
3. **可选参数**：注意区分必需参数和可选参数
4. **示例代码**：不是所有方法都有示例

## 测试选择器

使用以下命令测试选择器：

```bash
# 下载示例页面
python scripts/http_fetcher.py "https://sdk.freedo3d.com/doc/api/Marker.html" data/cache/Marker.html

# 解析并查看结果
python scripts/html_parser.py data/cache/Marker.html
```
