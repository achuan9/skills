# Personal Claude Code Skills Collection

A personal collection of Claude Code skills to enhance development productivity.

## 📦 Included Skills

### dts-docs-query

DTS SDK API documentation query tool with support for precise and natural language queries.

- **Features**: Query DTS SDK, freedo, and twin map related APIs
- **Capabilities**:
  - Precise query: `acApi.marker.add`
  - Natural language query: "How to add marker points"
  - Lazy crawling: Fetch documentation on-demand from official website
  - Local caching: Automatically cache queried APIs (7 days)
  - Smart error correction: Prompt users for correct URLs on 404 errors
  - Documentation export: Automatically generate Markdown documentation locally

For details: [skills/dts-docs-query/README.md](skills/dts-docs-query/README.md)

## 🚀 Installation

### Method 1: Via Plugin Marketplace (Recommended)

Execute the following commands in Claude Code:

```bash
# Add marketplace source
/plugin marketplace add https://github.com/achuan9/skills

# Install dts-docs-query skill
/plugin install dts-docs-query@achuan9-skills
```

After installation, the skill will be copied to:
```
C:\Users\{username}\.claude\plugins\cache\achuan9-skills\{commit}\
```

### Method 2: Manual Installation

```bash
# Clone repository
git clone https://github.com/achuan9/skills.git
cd skills

# Ensure skill is in the correct location
# skills/dts-docs-query/SKILL.md
```

## 📖 Usage Examples

### Query DTS SDK API

```
You: How to use acApi.marker.add?
You: How to add marker points in DTS?
You: What are all the methods of acApi.box?
```

Claude will automatically recognize keywords (DTS, acApi, freedo, twin, map) and trigger the skill.

### Command Line Testing

```bash
cd skills/dts-docs-query

# Query Marker class
python query.py acApi.marker

# Query specific method
python query.py acApi.marker add

# Show code examples only
python query.py acApi.marker add code-only
```

## 🛠️ Development Guide

### Adding a New Skill

1. Create a new skill directory under `skills/`
2. Create `SKILL.md` file (core configuration)
3. Implement related scripts and tools
4. Update this README.md
5. Update `.claude-plugin/marketplace.json`

### Skill Directory Structure

```
skills/
└── your-skill/
    ├── SKILL.md          # Required: skill configuration file
    ├── README.md         # Optional: skill documentation
    ├── query.py          # Optional: command line tool
    ├── scripts/          # Optional: helper scripts
    ├── references/       # Optional: reference documentation
    └── data/             # Optional: data directory
```

## 📋 Requirements

### Python Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies:
- `requests>=2.31.0` - HTTP requests
- `beautifulsoup4>=4.12.0` - HTML parsing
- `lxml>=4.9.0` - XML/HTML parser
- `chardet>=5.0.0` - Character encoding detection

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [DTS SDK Official Documentation](https://sdk.freedo3d.com/doc/api/)
- [Claude Code Official Documentation](https://docs.anthropic.com/claude-code)

---

