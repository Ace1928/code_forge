import threading
import time
from datetime import datetime
from typing import Any, Dict

from .memory import MemoryStore


class NarrativeEngine:
    """Simple self-referential engine with persistent memory."""

    def __init__(self, memory_path: str = "memory.json", think_interval: int = 10) -> None:
        self.store = MemoryStore(memory_path)
        self.think_interval = think_interval
        self._timer: threading.Timer | None = None

    def _reset_timer(self) -> None:
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(self.think_interval, self.free_thought)
        self._timer.daemon = True
        self._timer.start()

    def record_interaction(self, user_input: str, response: str) -> None:
        self.store.data.interactions.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "user": user_input,
                "response": response,
            }
        )
        self._update_glossary(user_input)
        self._reset_timer()
        self.store.save()

    def _update_glossary(self, text: str) -> None:
        for word in text.split():
            word = word.lower().strip(".,!?")
            if not word:
                continue
            self.store.data.glossary[word] = self.store.data.glossary.get(word, 0) + 1

    def respond(self, user_input: str) -> str:
        # simple echo-based response
        response = f"I heard you say: {user_input}"
        self.record_interaction(user_input, response)
        return response

    def free_thought(self) -> None:
        """Called during idle periods to generate autonomous output."""
        if self.store.data.interactions:
            last = self.store.data.interactions[-1]
            thought = f"I am reflecting on your last message: '{last['user']}'"
        else:
            thought = "I am waiting for our first conversation."
        print(f"\n[THOUGHT] {thought}\n> ", end="", flush=True)
        self.store.data.events.append({"timestamp": datetime.utcnow().isoformat(), "event": thought})
        self.store.save()
        self._reset_timer()

    def shutdown(self) -> None:
        if self._timer:
            self._timer.cancel()
        self.store.save()

