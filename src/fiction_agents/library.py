"""
AgentLibrary class - manages and provides access to all fiction writing agents.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from .agent import FictionAgent


class AgentLibrary:
    """Library for managing short fiction writing agents.

    Loads agent configurations from JSON files and provides
    methods to search, filter, and retrieve agents for use
    with Edge browser Copilot sidebar.

    Example usage:
        library = AgentLibrary()
        agent = library.get_agent("story_planner")
        print(agent.get_edge_copilot_prompt())
    """

    _DEFAULT_AGENTS_DIR = Path(__file__).parent.parent.parent / "agents"

    def __init__(self, agents_dir: Optional[str] = None):
        """Initialize the library.

        Args:
            agents_dir: Path to directory containing agent JSON files.
                        Defaults to the bundled agents directory.
        """
        self._agents_dir = Path(agents_dir) if agents_dir else self._DEFAULT_AGENTS_DIR
        self._agents: Dict[str, FictionAgent] = {}
        self._load_agents()

    def _load_agents(self) -> None:
        """Load all agent configurations from the agents directory."""
        if not self._agents_dir.exists():
            return
        for json_file in sorted(self._agents_dir.glob("*.json")):
            try:
                with open(json_file, encoding="utf-8") as f:
                    data = json.load(f)
                agent = FictionAgent.from_dict(data)
                self._agents[agent.id] = agent
            except (json.JSONDecodeError, KeyError) as e:
                raise ValueError(f"Failed to load agent from {json_file}: {e}") from e

    def get_agent(self, agent_id: str) -> Optional[FictionAgent]:
        """Get an agent by its ID.

        Args:
            agent_id: The unique identifier of the agent.

        Returns:
            The FictionAgent instance, or None if not found.
        """
        return self._agents.get(agent_id)

    def list_agents(self) -> List[FictionAgent]:
        """Return a list of all available agents.

        Returns:
            List of all FictionAgent instances.
        """
        return list(self._agents.values())

    def search_by_tag(self, tag: str) -> List[FictionAgent]:
        """Find agents that have a specific tag.

        Args:
            tag: Tag to search for.

        Returns:
            List of matching FictionAgent instances.
        """
        return [agent for agent in self._agents.values() if tag in agent.tags]

    def search_by_genre(self, genre: str) -> List[FictionAgent]:
        """Find agents that support a specific genre.

        Args:
            genre: Genre to search for (e.g., '科幻', '悬疑').

        Returns:
            List of matching FictionAgent instances.
        """
        return [
            agent
            for agent in self._agents.values()
            if genre in agent.genre or "通用" in agent.genre
        ]

    def get_all_tags(self) -> List[str]:
        """Return a sorted list of all unique tags across all agents.

        Returns:
            Sorted list of unique tag strings.
        """
        tags = set()
        for agent in self._agents.values():
            tags.update(agent.tags)
        return sorted(tags)

    def get_all_genres(self) -> List[str]:
        """Return a sorted list of all unique genres across all agents.

        Returns:
            Sorted list of unique genre strings.
        """
        genres = set()
        for agent in self._agents.values():
            genres.update(agent.genre)
        return sorted(genres)

    def export_for_edge_copilot(self, language: str = "zh") -> List[dict]:
        """Export all agents in a format suitable for Edge Copilot sidebar.

        Args:
            language: Language code, 'zh' for Chinese, 'en' for English.

        Returns:
            List of agent dictionaries with Copilot-ready prompts.
        """
        result = []
        for agent in self._agents.values():
            result.append(
                {
                    "id": agent.id,
                    "name": agent.name if language == "zh" else agent.name_en,
                    "description": (
                        agent.description if language == "zh" else agent.description_en
                    ),
                    "system_prompt": agent.get_edge_copilot_prompt(language),
                    "example_prompts": agent.example_prompts,
                    "instruction": agent.edge_copilot_instruction,
                }
            )
        return result

    def __len__(self) -> int:
        return len(self._agents)

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self._agents
