import threading
import time
from datetime import datetime
from typing import Any, Dict, Optional

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
except Exception:  # pragma: no cover - optional dependency
    AutoModelForCausalLM = None  # type: ignore
    AutoTokenizer = None  # type: ignore
    pipeline = None  # type: ignore

from .memory import MemoryStore


class NarrativeEngine:
    """Self-referential engine backed by a language model."""

    def __init__(
        self,
        memory_path: str = "memory.json",
        think_interval: int = 10,
        model_name: str = "Qwen/Qwen1.5-0.5B",
        max_tokens: int = 60,
    ) -> None:
        self.store = MemoryStore(memory_path)
        self.think_interval = think_interval
        self.model_name = model_name
        self.max_tokens = max_tokens
        self._timer: Optional[threading.Timer] = None
        self._pipeline = self._load_model()

    def _load_model(self):
        if not AutoModelForCausalLM:
            print("Warning: transformers not installed. Falling back to echo mode.")
            return None
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name)
            return pipeline("text-generation", model=model, tokenizer=tokenizer)
        except Exception as exc:
            print(f"Warning: failed to load model {self.model_name}: {exc}. Using echo mode.")
            return None

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
        if self._pipeline:
            try:
                result = self._pipeline(
                    user_input, max_new_tokens=self.max_tokens, do_sample=True
                )
                response = result[0]["generated_text"]
            except Exception as exc:  # pragma: no cover - runtime guard
                print(f"Model inference failed: {exc}. Falling back to echo.")
                response = f"I heard you say: {user_input}"
        else:
            response = f"I heard you say: {user_input}"
        self.record_interaction(user_input, response)
        return response

    def free_thought(self) -> None:
        """Called during idle periods to generate autonomous output."""
        if self.store.data.interactions:
            last = self.store.data.interactions[-1]
            prompt = f"Reflect on this message: {last['user']}"
        else:
            prompt = "Introduce yourself."

        if self._pipeline:
            try:
                result = self._pipeline(
                    prompt, max_new_tokens=self.max_tokens, do_sample=True
                )
                thought = result[0]["generated_text"]
            except Exception as exc:  # pragma: no cover - runtime guard
                print(f"Model inference failed during free thought: {exc}")
                thought = prompt
        else:
            thought = prompt

        print(f"\n[THOUGHT] {thought}\n> ", end="", flush=True)
        self.store.data.events.append({"timestamp": datetime.utcnow().isoformat(), "event": thought})
        self.store.save()
        self._reset_timer()

    def shutdown(self) -> None:
        if self._timer:
            self._timer.cancel()
        self.store.save()

