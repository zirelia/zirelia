# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import yaml
import json
from typing import Dict, Any, List
from .memory import MemoryManager

class PersonaEngine:
    def __init__(self, config_path: str = "config/persona.yaml"):
        self.config = self._load_config(config_path)
        self.memory = MemoryManager()
        self.memory.load_memory()

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Loads persona configuration from YAML."""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Fallback for testing if config doesn't exist
            return {"name": "Test Persona", "traits": [], "voice": {"tone": "Standard"}}

    def generate_response(self, user_input: str, platform: str = "general") -> str:
        """
        Generates a response based on persona, memory, and platform context.
        This function would typically call an LLM API.
        """
        # 1. Retrieve context
        context = self.memory.retrieve_context(user_input)

        # 2. Construct prompt (Conceptually)
        prompt = self._construct_prompt(user_input, context, platform)

        # 3. Call LLM (Mocked here)
        response = self._mock_llm_response(prompt)

        # 4. Update short-term memory
        self.memory.add_short_term({"role": "user", "content": user_input})
        self.memory.add_short_term({"role": "assistant", "content": response})

        return response

    def _construct_prompt(self, user_input: str, context: Dict[str, Any], platform: str) -> str:
        """Constructs the prompt for the LLM."""
        traits = ", ".join(self.config.get("traits", []))
        tone = self.config.get("voice", {}).get("tone", "neutral")

        base_prompt = f"""
        You are {self.config.get('name')}.
        Traits: {traits}
        Tone: {tone}
        Platform: {platform}

        Recent Context: {json.dumps(context['recent_interactions'])}

        User says: {user_input}
        Response:
        """
        return base_prompt

    def _mock_llm_response(self, prompt: str) -> str:
        """Mock LLM response for demonstration."""
        # In production, this would be:
        # response = openai.ChatCompletion.create(...)
        return "That's so interesting! Tell me more about it. ✨ #DigitalLife"

    def get_personality_summary(self) -> str:
        """Returns a summary of the persona."""
        return f"{self.config.get('name')} - {self.config.get('occupation')}"
