"""
示例：如何使用短篇小说创作智能体库
Example: How to use the Fiction Writing Agents Library
"""

import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fiction_agents import AgentLibrary


def main():
    # Initialize the library
    library = AgentLibrary()

    print("=" * 60)
    print("短篇小说创作智能体库 / Fiction Writing Agents Library")
    print("=" * 60)
    print(f"\n共有 {len(library)} 个智能体 / {len(library)} agents available\n")

    # List all agents
    print("可用智能体列表 / Available Agents:")
    print("-" * 40)
    for agent in library.list_agents():
        print(f"  [{agent.id}] {agent.name} / {agent.name_en}")
        print(f"    {agent.description[:50]}...")
        print()

    # Get a specific agent and show its Edge Copilot prompt
    print("=" * 60)
    print("示例：故事策划师的 Edge Copilot 提示词")
    print("Example: Story Planner's Edge Copilot prompt")
    print("=" * 60)

    agent = library.get_agent("story_planner")
    if agent:
        print(f"\n智能体: {agent.name}")
        print(f"描述: {agent.description}\n")
        print("--- Edge Copilot 系统提示词 (中文) ---")
        print(agent.get_edge_copilot_prompt("zh"))
        print("\n--- 示例提问 / Example Prompts ---")
        for i, prompt in enumerate(agent.example_prompts, 1):
            print(f"  {i}. {prompt}")

    # Search by genre
    print("\n" + "=" * 60)
    print("搜索支持'悬疑'类型的智能体 / Search agents for '悬疑' genre")
    print("=" * 60)
    mystery_agents = library.search_by_genre("悬疑")
    for agent in mystery_agents:
        print(f"  ✓ {agent.name} ({agent.id})")

    # Export for Edge Copilot
    print("\n" + "=" * 60)
    print("导出 Edge Copilot 配置 / Export Edge Copilot Configuration")
    print("=" * 60)
    copilot_config = library.export_for_edge_copilot("zh")
    print(f"\n已导出 {len(copilot_config)} 个智能体的配置")
    print("可将各智能体的 system_prompt 复制到 Edge 浏览器 Copilot 侧边栏使用")


if __name__ == "__main__":
    main()
