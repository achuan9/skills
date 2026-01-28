# DTS SDK Skills Collection

Claude Code Skills 集合，提升开发效率。

## 📦 包含的 Skills

### dts-docs-query

DTS SDK API 文档查询工具，支持精确查询和自然语言查询。

- **功能**：查询 DTS SDK、freedo、孪生地图相关 API
- **特性**：
  - 精确查询：`acApi.marker.add`
  - 自然语言查询："如何添加标注点"
  - 惰性爬取：按需从官网获取文档
  - 本地缓存：自动缓存已查询的 API（7天）
  - 智能纠错：404 时提示用户提供正确的 URL
  - 文档导出：自动生成 Markdown 文档到本地

详细说明：[skills/dts-docs-query/README.md](skills/dts-docs-query/README.md)

## 🚀 安装方式

### 方式 1：通过 Plugin Marketplace 安装（推荐）

在 Claude Code 中执行以下命令：

```bash
# 添加 marketplace 源
/plugin marketplace add https://github.com/achuan9/skills

# 安装 dts-docs-query skill
/plugin install dts-docs-query@dts-sdk-skills
```

安装后 skill 会被复制到：
```
C:\Users\{username}\.claude\plugins\cache\dts-sdk-skills\{commit}\
```

### 方式 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/achuan9/skills.git
cd skills

# 确保 skill 在正确位置
# skills/dts-docs-query/SKILL.md
```

## 📖 使用示例

### 查询 DTS SDK API

```
你：acApi.marker.add 如何使用？
你：如何在 DTS 中添加标注点？
你：acApi.box 的所有方法有哪些？
```

Claude 会自动识别关键词（DTS、acApi、freedo、孪生、地图）并触发 skill。

### 命令行测试

```bash
cd skills/dts-docs-query

# 查询 Marker 类
python query.py acApi.marker

# 查询特定方法
python query.py acApi.marker add

# 只显示代码示例
python query.py acApi.marker add code-only
```

## 🛠️ 开发指南

### 添加新 Skill

1. 在 `skills/` 目录下创建新的 skill 目录
2. 创建 `SKILL.md` 文件（核心配置）
3. 实现相关脚本和工具
4. 更新本 README.md
5. 更新 `.claude-plugin/marketplace.json`

### Skill 目录结构

```
skills/
└── your-skill/
    ├── SKILL.md          # 必需：skill 配置文件
    ├── README.md         # 可选：skill 说明文档
    ├── query.py          # 可选：命令行工具
    ├── scripts/          # 可选：辅助脚本
    ├── references/       # 可选：参考文档
    └── data/             # 可选：数据目录
```

## 📋 依赖要求

### Python 依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- `requests>=2.31.0` - HTTP 请求
- `beautifulsoup4>=4.12.0` - HTML 解析
- `lxml>=4.9.0` - XML/HTML 解析器
- `chardet>=5.0.0` - 字符编码检测

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🔗 相关链接

- [DTS SDK 官方文档](https://sdk.freedo3d.com/doc/api/)
- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)

---
