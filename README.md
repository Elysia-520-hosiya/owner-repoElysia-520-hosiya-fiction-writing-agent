# 短篇小说创作智能体库 / Fiction Writing Agents Library

一个专为 **Edge 浏览器 Copilot 侧边栏**设计的短篇小说创作智能体库。  
A library of short fiction writing AI agents designed for use with the **Edge browser Copilot sidebar**.

---

## 📖 简介 / Introduction

本库提供一系列专业的短篇小说创作智能体，每个智能体针对小说创作的不同环节，包含精心设计的系统提示词（System Prompt），可直接在 Edge 浏览器的 Copilot 侧边栏中使用。

This library provides a collection of specialized short fiction writing agents. Each agent targets a different aspect of story writing, containing carefully crafted system prompts that can be used directly in the Edge browser's Copilot sidebar.

---

## 🤖 智能体列表 / Available Agents

| ID | 名称 | Name | 功能 |
|----|------|------|------|
| `story_planner` | 故事策划师 | Story Planner | 规划故事结构、主题和情节大纲 |
| `character_creator` | 人物塑造师 | Character Creator | 创建立体真实的小说人物 |
| `plot_developer` | 情节发展师 | Plot Developer | 设计冲突、转折和高潮 |
| `dialogue_writer` | 对话写作师 | Dialogue Writer | 撰写自然生动的人物对话 |
| `scene_writer` | 场景描写师 | Scene Writer | 创作沉浸式场景描写 |
| `story_editor` | 故事编辑师 | Story Editor | 全面审阅和优化故事 |

---

## 🚀 在 Edge Copilot 侧边栏中使用 / Using with Edge Copilot Sidebar

### 方法一：直接使用提示词

1. 打开 **Edge 浏览器**，点击右上角的 Copilot 图标（或按 `Ctrl+Shift+.`）
2. 从 `agents/` 目录中选择对应的 JSON 文件
3. 复制 `system_prompt` 字段的内容
4. 在 Copilot 侧边栏的对话框中粘贴提示词，开始创作

### Method 1: Direct Prompt Usage

1. Open **Edge browser**, click the Copilot icon (or press `Ctrl+Shift+.`)
2. Choose the desired agent from the `agents/` directory
3. Copy the content of the `system_prompt` field
4. Paste the prompt in the Copilot sidebar chat box and start writing

### 方法二：使用 Python 库

```python
from fiction_agents import AgentLibrary

# 初始化库
library = AgentLibrary()

# 获取故事策划师智能体
agent = library.get_agent("story_planner")

# 获取适合 Edge Copilot 的提示词（中文）
prompt = agent.get_edge_copilot_prompt("zh")
print(prompt)
```

### Method 2: Using the Python Library

```python
from fiction_agents import AgentLibrary

# Initialize the library
library = AgentLibrary()

# Get the story planner agent
agent = library.get_agent("story_planner")

# Get the prompt for Edge Copilot (English)
prompt = agent.get_edge_copilot_prompt("en")
print(prompt)
```

---

## 📁 项目结构 / Project Structure

```
fiction-writing-agents/
├── agents/                    # Agent configuration JSON files
│   ├── story_planner.json     # 故事策划师
│   ├── character_creator.json # 人物塑造师
│   ├── plot_developer.json    # 情节发展师
│   ├── dialogue_writer.json   # 对话写作师
│   ├── scene_writer.json      # 场景描写师
│   └── story_editor.json      # 故事编辑师
├── src/
│   └── fiction_agents/        # Python package
│       ├── __init__.py
│       ├── agent.py           # FictionAgent class
│       └── library.py         # AgentLibrary class
├── examples/
│   └── basic_usage.py         # Usage example
├── tests/
│   └── test_fiction_agents.py # Tests
├── pyproject.toml
└── README.md
```

---

## 🛠️ 安装和使用 / Installation and Usage

### 安装依赖 / Install Dependencies

```bash
# Python 3.8+ required
pip install -e .
```

### 运行示例 / Run Example

```bash
python examples/basic_usage.py
```

### 运行测试 / Run Tests

```bash
pip install pytest
pytest tests/
```

---

## 📝 智能体 JSON 格式 / Agent JSON Format

每个智能体配置文件包含以下字段：

```json
{
  "id": "unique_agent_id",
  "name": "智能体名称（中文）",
  "name_en": "Agent Name (English)",
  "description": "功能描述（中文）",
  "description_en": "Description (English)",
  "system_prompt": "中文系统提示词",
  "system_prompt_en": "English system prompt",
  "version": "1.0.0",
  "example_prompts": ["示例提问1", "示例提问2"],
  "tags": ["标签1", "标签2"],
  "genre": ["通用", "科幻", "悬疑"],
  "edge_copilot_instruction": "在 Edge Copilot 中的使用说明"
}
```

---

## 🔍 Python API 参考 / Python API Reference

### `AgentLibrary`

```python
library = AgentLibrary(agents_dir=None)

# Get all agents
agents = library.list_agents()

# Get agent by ID
agent = library.get_agent("story_planner")

# Search by tag
results = library.search_by_tag("对话")

# Search by genre
results = library.search_by_genre("科幻")

# Export for Edge Copilot
config = library.export_for_edge_copilot(language="zh")  # or "en"
```

### `FictionAgent`

```python
# Get Edge Copilot prompt
prompt_zh = agent.get_edge_copilot_prompt("zh")
prompt_en = agent.get_edge_copilot_prompt("en")

# Convert to/from dict
data = agent.to_dict()
agent = FictionAgent.from_dict(data)
```

---

## 📚 支持的体裁 / Supported Genres

`通用` `科幻` `奇幻` `悬疑` `惊悚` `爱情` `现实主义` `历史`

---

## 📄 许可证 / License

MIT License
