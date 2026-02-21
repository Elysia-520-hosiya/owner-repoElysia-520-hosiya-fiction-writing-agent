"""
Tests for the Fiction Writing Agents library.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fiction_agents import AgentLibrary, FictionAgent


REPO_ROOT = Path(__file__).parent.parent
AGENTS_DIR = REPO_ROOT / "agents"


class TestFictionAgent:
    """Tests for the FictionAgent class."""

    def _make_agent_data(self, **kwargs):
        data = {
            "id": "test_agent",
            "name": "测试智能体",
            "name_en": "Test Agent",
            "description": "测试描述",
            "description_en": "Test description",
            "system_prompt": "你是一个测试助手。",
            "system_prompt_en": "You are a test assistant.",
            "version": "1.0.0",
            "example_prompts": ["示例提示"],
            "tags": ["测试"],
            "genre": ["通用"],
            "edge_copilot_instruction": "测试使用说明",
        }
        data.update(kwargs)
        return data

    def test_from_dict_creates_agent(self):
        data = self._make_agent_data()
        agent = FictionAgent.from_dict(data)
        assert agent.id == "test_agent"
        assert agent.name == "测试智能体"
        assert agent.name_en == "Test Agent"

    def test_from_dict_defaults(self):
        """from_dict should handle optional fields with defaults."""
        data = {
            "id": "minimal",
            "name": "最小",
            "name_en": "Minimal",
            "description": "desc",
            "system_prompt": "prompt",
        }
        agent = FictionAgent.from_dict(data)
        assert agent.version == "1.0.0"
        assert agent.example_prompts == []
        assert agent.tags == []
        assert agent.genre == []

    def test_to_dict_roundtrip(self):
        data = self._make_agent_data()
        agent = FictionAgent.from_dict(data)
        result = agent.to_dict()
        assert result["id"] == data["id"]
        assert result["name"] == data["name"]
        assert result["system_prompt"] == data["system_prompt"]

    def test_get_edge_copilot_prompt_zh(self):
        data = self._make_agent_data()
        agent = FictionAgent.from_dict(data)
        assert agent.get_edge_copilot_prompt("zh") == "你是一个测试助手。"

    def test_get_edge_copilot_prompt_en(self):
        data = self._make_agent_data()
        agent = FictionAgent.from_dict(data)
        assert agent.get_edge_copilot_prompt("en") == "You are a test assistant."

    def test_get_edge_copilot_prompt_default_is_zh(self):
        data = self._make_agent_data()
        agent = FictionAgent.from_dict(data)
        assert agent.get_edge_copilot_prompt() == agent.get_edge_copilot_prompt("zh")

    def test_str_representation(self):
        data = self._make_agent_data()
        agent = FictionAgent.from_dict(data)
        assert "test_agent" in str(agent)
        assert "测试智能体" in str(agent)


class TestAgentLibrary:
    """Tests for the AgentLibrary class."""

    def test_library_loads_bundled_agents(self):
        library = AgentLibrary()
        assert len(library) > 0

    def test_library_contains_expected_agents(self):
        library = AgentLibrary()
        expected_ids = [
            "story_planner",
            "character_creator",
            "plot_developer",
            "dialogue_writer",
            "story_editor",
            "scene_writer",
        ]
        for agent_id in expected_ids:
            assert agent_id in library, f"Agent '{agent_id}' not found in library"

    def test_get_agent_returns_correct_agent(self):
        library = AgentLibrary()
        agent = library.get_agent("story_planner")
        assert agent is not None
        assert agent.id == "story_planner"

    def test_get_agent_returns_none_for_unknown(self):
        library = AgentLibrary()
        assert library.get_agent("nonexistent_agent") is None

    def test_list_agents_returns_all(self):
        library = AgentLibrary()
        agents = library.list_agents()
        assert len(agents) == len(library)
        assert all(isinstance(a, FictionAgent) for a in agents)

    def test_search_by_tag(self):
        library = AgentLibrary()
        results = library.search_by_tag("对话")
        assert len(results) > 0
        assert all("对话" in a.tags for a in results)

    def test_search_by_genre_universal(self):
        """Agents with '通用' genre should appear in any genre search."""
        library = AgentLibrary()
        results = library.search_by_genre("科幻")
        assert len(results) > 0

    def test_get_all_tags(self):
        library = AgentLibrary()
        tags = library.get_all_tags()
        assert isinstance(tags, list)
        assert len(tags) > 0
        assert tags == sorted(tags)

    def test_get_all_genres(self):
        library = AgentLibrary()
        genres = library.get_all_genres()
        assert isinstance(genres, list)
        assert "通用" in genres

    def test_export_for_edge_copilot_zh(self):
        library = AgentLibrary()
        export = library.export_for_edge_copilot("zh")
        assert len(export) == len(library)
        for item in export:
            assert "id" in item
            assert "name" in item
            assert "system_prompt" in item
            assert "example_prompts" in item

    def test_export_for_edge_copilot_en(self):
        library = AgentLibrary()
        export = library.export_for_edge_copilot("en")
        assert len(export) > 0
        for item in export:
            assert "system_prompt" in item

    def test_custom_agents_dir(self):
        """Library should work with a custom agents directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent_data = {
                "id": "custom_agent",
                "name": "自定义智能体",
                "name_en": "Custom Agent",
                "description": "custom",
                "description_en": "custom",
                "system_prompt": "custom prompt",
                "system_prompt_en": "custom prompt en",
            }
            agent_file = Path(tmpdir) / "custom_agent.json"
            agent_file.write_text(json.dumps(agent_data), encoding="utf-8")

            library = AgentLibrary(agents_dir=tmpdir)
            assert len(library) == 1
            assert "custom_agent" in library

    def test_contains_operator(self):
        library = AgentLibrary()
        assert "story_planner" in library
        assert "nonexistent" not in library


class TestAgentJsonFiles:
    """Tests that validate the JSON agent files are well-formed."""

    @pytest.mark.parametrize(
        "agent_file",
        list(AGENTS_DIR.glob("*.json")),
        ids=lambda p: p.stem,
    )
    def test_agent_file_is_valid_json(self, agent_file):
        with open(agent_file, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    @pytest.mark.parametrize(
        "agent_file",
        list(AGENTS_DIR.glob("*.json")),
        ids=lambda p: p.stem,
    )
    def test_agent_file_has_required_fields(self, agent_file):
        required_fields = ["id", "name", "name_en", "description", "system_prompt"]
        with open(agent_file, encoding="utf-8") as f:
            data = json.load(f)
        for field in required_fields:
            assert field in data, f"Missing field '{field}' in {agent_file.name}"

    @pytest.mark.parametrize(
        "agent_file",
        list(AGENTS_DIR.glob("*.json")),
        ids=lambda p: p.stem,
    )
    def test_agent_file_id_matches_filename(self, agent_file):
        with open(agent_file, encoding="utf-8") as f:
            data = json.load(f)
        assert data["id"] == agent_file.stem, (
            f"Agent id '{data['id']}' does not match filename '{agent_file.stem}'"
        )

    @pytest.mark.parametrize(
        "agent_file",
        list(AGENTS_DIR.glob("*.json")),
        ids=lambda p: p.stem,
    )
    def test_agent_file_loads_as_fiction_agent(self, agent_file):
        with open(agent_file, encoding="utf-8") as f:
            data = json.load(f)
        agent = FictionAgent.from_dict(data)
        assert isinstance(agent, FictionAgent)
        assert agent.id == agent_file.stem
