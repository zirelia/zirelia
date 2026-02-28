# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate       
from langchain_core.output_parsers import StrOutputParser
from config.settings import get_settings
from core.utils.logger import logger
import yaml
import os

# Avoid circular/implicit import
from core.persona.memory_vector import VectorMemory

class PersonaBrain:
    def __init__(self, config_path: str = "config/persona.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f) or {}
        self.settings = get_settings()
        
        # Check for dummy key or missing key
        if not self.settings.OPENAI_API_KEY or "dummy" in self.settings.OPENAI_API_KEY:
            logger.warning("ðŸ§  LLM Warning: Using Mock LLM (Dummy API Key detected)")
            from langchain_community.llms.fake import FakeListLLM
            self.llm = FakeListLLM(responses=["This is a mock generated thought about the context."])
        else:
            model_name = self.config.get("parameters", {}).get("model", "gpt-4o")
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=self.config.get("parameters", {}).get("temperature", 0.7),
                max_tokens=self.config.get("parameters", {}).get("max_tokens", 256),
                api_key=self.settings.OPENAI_API_KEY
            )
            
        self.memory = VectorMemory()
        self.system_prompt = self._build_system_prompt()
        logger.info("PersonaBrain initialized.")

    def _build_system_prompt(self) -> str:
        """
        Constructs the overarching system prompt from persona.yaml configurations.
        """
        name = self.config.get("name", "AI")
        role = self.config.get("role", "Assistant")
        traits = ", ".join(self.config.get("traits", []))
        backstory = self.config.get("backstory", "")
        style = self.config.get("style", {})
        
        tone = style.get("tone", "")
        formatting = style.get("formatting", "")
        hashtags = ", ".join(style.get("hashtags", []))
        
        prompt = f"""
You are {name}, a {role}.
Your core traits: {traits}.

Backstory:
{backstory}

Tone & Style Guidelines:
- Tone: {tone}
- Formatting: {formatting}
- Typical Hashtags: {hashtags}

Act and respond EXACTLY as {name}. NEVER break character.
NEVER refer to yourself as an AI or an assistant.
"""
        return prompt

    def generate_thought(self, context: str, platform: str) -> str:
        """
        Generates a thought or drafted content based on context.
        """
        # 1. Retrieve relevant memories
        memories = self.memory.search_memory(context, n_results=3)
        memory_context = "\n".join(memories) if memories else "No specific memory found."

        # 2. Platform-Specific Formatting Rules
        p_lower = platform.lower()
        if p_lower == "instagram":
            platform_instructions = "Write a long, descriptive, and emotional caption. Include 15-20 relevant hashtags at the end. Use emojis."
        elif p_lower == "threads":
            platform_instructions = (
                "You are posting on Threads. Your goal is MAXIMUM ENGAGEMENT.\n"
                "Write something that people MUST reply to. Use one of these formats:\n"
                "1) A hot take or unpopular opinion\n"
                "2) A 'this or that' question\n"
                "3) A relatable rant/complaint\n"
                "4) A mysterious tease about new IG content\n"
                "5) A random shower thought\n"
                "Rules: Under 300 chars. No hashtags. Casual slang. "
                "End with a hook that demands a reply. Never say 'check out my Instagram'."
            )
            # Cross-promo: when Threads has image content, add subtle IG tease
            if "Image Description" in context:
                platform_instructions += (
                    "\nSince this post has a photo, subtly hint that more content "
                    "is on your Instagram. Never use 'link in bio' or direct URLs. "
                    "Example: '...the full set? you know where to find it 😏'"
                )
        elif p_lower == "twitter":
            platform_instructions = "Write a short, punchy, slightly edgy/shitpost style tweet. Maximum 280 characters. 1-2 hashtags max."
        elif p_lower == "facebook":
            platform_instructions = "Write a conversational, friendly, and informal post aimed at a broader audience. 2-3 hashtags."
        else:
            platform_instructions = "Write a standard social media post."

        # 3. Construct Prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            HumanMessagePromptTemplate.from_template(
                """
                Platform: {platform}
                Current Context/Visual Scene: {context}
                
                Relevant Memories/Past Context:
                {memory_context}
                
                FORMATTING RULES FOR THIS PLATFORM (Follow strictly):
                {platform_instructions}
                
                Write the post:
                """
            )
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            response = chain.invoke({
                "platform": platform, 
                "context": context,
                "memory_context": memory_context,
                "platform_instructions": platform_instructions
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
                7. CONTENT SAFETY: NEVER describe lingerie, underwear, bikinis, or revealing intimate clothing. Keep outfits appropriate: casual wear, athletic wear, streetwear, dresses, or professional attire.
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
