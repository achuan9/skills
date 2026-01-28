# DTS SDK API 结构说明

## URL 拼接规则

基础 URL：`https://sdk.freedo3d.com/doc/api/`

## API 路径到类名的映射

| API 路径 | 类名 | URL |
|---------|------|-----|
| acApi.marker | Marker | Marker.html |
| acApi.box | Box | Box.html |
| acApi.model | Model | Model.html |
| acApi.camera | Camera | Camera.html |

## 解析逻辑

### 步骤 1：提取模块名

从 `acApi.module.method` 中提取 `module` 部分：
- `acApi.marker.add` → `marker`
- `acApi.box.create` → `box`

### 步骤 2：转换为类名

将首字母大写：
- `marker` → `Marker`
- `box` → `Box`

### 步骤 3：拼接 URL

```
{base_url}{ClassName}.html
```

示例：
- `Marker` → `https://sdk.freedo3d.com/doc/api/Marker.html`
- `Box` → `https://sdk.freedo3d.com/doc/api/Box.html`

## 注意事项

1. **忽略方法名**：查询 `acApi.marker.add` 和 `acApi.marker` 都会请求 `Marker.html`
2. **大小写不敏感**：`marker` 和 `Marker` 都映射到 `Marker.html`
3. **自定义映射**：如果默认映射失败，检查 `data/url_mappings.json` 中的用户自定义映射
