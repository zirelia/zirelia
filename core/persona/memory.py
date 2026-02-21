# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import json
from typing import List, Dict, Any

class MemoryManager:
    def __init__(self, persistence_path: str = "memory.json"):
        self.persistence_path = persistence_path
        self.short_term_memory: List[Dict[str, Any]] = []
        self.long_term_memory: List[Dict[str, Any]] = []
        # In a real implementation, long_term_memory would be connected to a Vector DB

    def add_short_term(self, interaction: Dict[str, Any]):
        """Adds a recent interaction to short-term memory."""
        self.short_term_memory.append(interaction)
        # Keep only last 10 interactions
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)

    def add_long_term(self, fact: Dict[str, Any]):
        """Adds a core fact or important memory to long-term storage."""
        self.long_term_memory.append(fact)
        self._save_memory()

    def retrieve_context(self, query: str = None) -> Dict[str, Any]:
        """Retrieves relevant context for the current situation."""
        # In a real system, this would do a semantic search on long_term_memory
        # and combine it with short_term_memory.
        return {
            "recent_interactions": self.short_term_memory,
            "core_facts": self.long_term_memory
        }

    def _save_memory(self):
        """Persists memory to disk (simple JSON dump for now)."""
        try:
            with open(self.persistence_path, 'w') as f:
                json.dump({
                    "short_term": self.short_term_memory,
                    "long_term": self.long_term_memory
                }, f)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def load_memory(self):
        """Loads memory from disk."""
        try:
            with open(self.persistence_path, 'r') as f:
                data = json.load(f)
                self.short_term_memory = data.get("short_term", [])
                self.long_term_memory = data.get("long_term", [])
        except FileNotFoundError:
            pass
