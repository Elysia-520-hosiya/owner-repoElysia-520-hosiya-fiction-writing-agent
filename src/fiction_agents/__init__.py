"""
Fiction Writing Agents Library
短篇小说创作智能体库

A collection of AI agents for short fiction writing,
designed to work with Edge browser Copilot sidebar.
"""

from .agent import FictionAgent
from .library import AgentLibrary

__version__ = "1.0.0"
__all__ = ["FictionAgent", "AgentLibrary"]
