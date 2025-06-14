import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Memory:
    """Persistent memory structure for interactions, events and glossary."""

    interactions: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    glossary: Dict[str, int] = field(default_factory=dict)


class MemoryStore:
    """Handles loading and saving Memory to a JSON file."""

    def __init__(self, path: str = "memory.json") -> None:
        self.path = path
        self.data = Memory()
        self.load()

    def load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            self.data = Memory(**raw)
        else:
            self.data = Memory()

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(self.data.__dict__, fh, indent=2)

