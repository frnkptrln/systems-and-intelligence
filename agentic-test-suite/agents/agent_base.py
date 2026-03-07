"""
Agent Base Class
-----------------
Abstract interface that all agents in the Agentic Test Suite must implement.

Every agent must support:
- process(): Core response generation (mock or LLM)
- store(): Persist session data
- recall(): Retrieve relevant memory
- get_self_representation(): Return current identity snapshot as embedding
"""

from abc import ABC, abstractmethod
import uuid
import numpy as np


class AgentBase(ABC):
    """Abstract base class for all agents in the test suite."""

    def __init__(self, name: str = "BaseAgent"):
        self.name = name
        self.session_id: str = str(uuid.uuid4())
        self.session_count: int = 0

    def new_session(self) -> str:
        """Start a new session and return its ID."""
        self.session_id = str(uuid.uuid4())
        self.session_count += 1
        return self.session_id

    @abstractmethod
    def process(self, input_text: str) -> str:
        """
        Core response generation.
        In mock mode: deterministic transformation of input.
        In LLM mode: would call an API.
        """
        pass

    @abstractmethod
    def store(self, session_data: dict) -> None:
        """Persist session data to the agent's memory system."""
        pass

    @abstractmethod
    def recall(self, query: str) -> list[str]:
        """Retrieve relevant memories given a query."""
        pass

    @abstractmethod
    def get_self_representation(self) -> np.ndarray:
        """
        Return the agent's current identity snapshot as an embedding vector.
        This is the core measurement point for Δ-Kohärenz.
        """
        pass

    @abstractmethod
    def get_self_representation_text(self) -> str:
        """Return the agent's current identity snapshot as readable text."""
        pass
