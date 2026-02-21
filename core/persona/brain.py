# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from virtual_influencer_engine.config.settings import get_settings
from virtual_influencer_engine.core.utils.logger import logger
import yaml
import httpx # Explicit import

from virtual_influencer_engine.core.persona.memory_vector import VectorMemory

settings = get_settings()

class PersonaBrain:
    def __init__(self, config_path: str = "virtual_influencer_engine/config/persona.yaml"):
        self.config = self._load_config(config_path)
        # Check for dummy key or missing key
        if not settings.OPENAI_API_KEY or "dummy" in settings.OPENAI_API_KEY:
            logger.warning("Using Mock LLM (Dummy API Key detected)")
            from langchain_community.llms.fake import FakeListLLM
            self.llm = FakeListLLM(responses=["[Mock] This is a generated thought about the context."])
        else:
            self.llm = ChatOpenAI(
                model="gpt-4", 
                temperature=0.7,
                api_key=settings.OPENAI_API_KEY
            )
        self.memory = VectorMemory()
        self.system_prompt = self._build_system_prompt()
        logger.info(f"PersonaBrain initialized for: {self.config.get('name')}")

    def _load_config(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load persona config: {e}")
            return {}

    def _build_system_prompt(self) -> str:
        c = self.config
        voice = c.get('voice', {})
        
        traits = ", ".join(c.get('traits', []))
        interests = ", ".join(c.get('interests', []))
        tone = voice.get('tone', 'Neutral')
        style = voice.get('style', 'Standard')
        backstory = c.get('backstory', '')

        return f"""
        You are {c.get('name')}, a {c.get('age')} year old {c.get('nationality')} {c.get('occupation')}.
        
        Your Traits: {traits}
        Your Interests: {interests}
        
        Backstory:
        {backstory}
        
        Voice Tone: {tone}
        Writing Style: {style}
        
        You aren't an AI. You are a real person online. Never break character.
        """

    def generate_thought(self, context: str, platform: str) -> str:
        """
        Generates a thought or drafted content based on context.
        """
        # 1. Retrieve relevant memories
        memories = self.memory.search_memory(context, n_results=3)
        memory_context = "\n".join(memories) if memories else "No specific memory found."

        # 2. Construct Prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template(
                """
                Platform: {platform}
                Current Context: {context}
                
                Relevant Memories/Past Context:
                {memory_context}
                
                Write a post/thought:
                """
            )
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            response = chain.invoke({
                "platform": platform, 
                "context": context,
                "memory_context": memory_context
            })
            
            # 3. Save this new thought to memory
            self.memory.add_memory(
                text=str(response),
                metadata={"type": "thought", "platform": platform}
            )
            
            return response
        except Exception as e:
            logger.error(f"LLM Generation failed: {e}")
            return "I need more coffee... (Error generating thought)"

    def generate_visual_prompt(self, context: str) -> str:
        """
        Generates a detailed, cinematic visual description for image generation.
        Expands simple topics (e.g. "Coffee") into full scenes.
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template(
                """
                Task: Describe a scene for a photorealistic Instagram photo of yourself based on the topic below.
                
                Topic: {context}
                
                Guidelines:
                1. Focus on VIBE, OUTFIT, LIGHTING, and SCENERY.
                2. Keep it candid and natural (influencer style).
                3. Describe the pose clearly.
                4. CRITICAL: If holding something (cup, phone), try to describe the hands as resting or out of frame to avoid AI artifacts.
                5. Output ONLY the visual description. No hashtags, no "Here is the description".
                6. Length: 1-2 sentences max.
                """
            )
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            description = chain.invoke({
                "context": context
            })
            logger.info(f"🎨 Visual Prompt Expanded: '{description}'")
            return description
        except Exception as e:
            logger.error(f"Visual Prompt Generation failed: {e}")
            return f"Photo of {self.config.get('name')} doing {context}, cinematic lighting, candid."
