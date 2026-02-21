"""
FictionAgent class - represents a single short story writing agent.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FictionAgent:
    """Represents a short fiction writing AI agent.

    Each agent has a specific role in the story writing process
    and can be used with Edge browser Copilot sidebar.
    """

    id: str
    name: str
    name_en: str
    description: str
    description_en: str
    system_prompt: str
    system_prompt_en: str
    version: str = "1.0.0"
    example_prompts: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    genre: List[str] = field(default_factory=list)
    edge_copilot_instruction: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "FictionAgent":
        """Create a FictionAgent instance from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            name_en=data["name_en"],
            description=data["description"],
            description_en=data.get("description_en", ""),
            system_prompt=data["system_prompt"],
            system_prompt_en=data.get("system_prompt_en", ""),
            version=data.get("version", "1.0.0"),
            example_prompts=data.get("example_prompts", []),
            tags=data.get("tags", []),
            genre=data.get("genre", []),
            edge_copilot_instruction=data.get("edge_copilot_instruction", ""),
        )

    def to_dict(self) -> dict:
        """Convert the agent to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "description": self.description,
            "description_en": self.description_en,
            "system_prompt": self.system_prompt,
            "system_prompt_en": self.system_prompt_en,
            "version": self.version,
            "example_prompts": self.example_prompts,
            "tags": self.tags,
            "genre": self.genre,
            "edge_copilot_instruction": self.edge_copilot_instruction,
        }

    def get_edge_copilot_prompt(self, language: str = "zh") -> str:
        """Get the system prompt formatted for Edge Copilot sidebar.

        Args:
            language: Language code, 'zh' for Chinese, 'en' for English.

        Returns:
            Formatted system prompt string for use in Edge Copilot.
        """
        if language == "en":
            return self.system_prompt_en
        return self.system_prompt

    def __str__(self) -> str:
        return f"FictionAgent(id={self.id!r}, name={self.name!r})"

    def __repr__(self) -> str:
        return self.__str__()
