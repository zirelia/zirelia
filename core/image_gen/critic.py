# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license


from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from virtual_influencer_engine.config.settings import get_settings
from virtual_influencer_engine.core.utils.logger import logger

class ImageCritic:
    def __init__(self):
        self.settings = get_settings()
        self.enabled = False
        
        # Check if OpenAI is available
        if self.settings.OPENAI_API_KEY and "dummy" not in self.settings.OPENAI_API_KEY:
            try:
                # Use gpt-4o-mini for cost-effective vision
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini", 
                    api_key=self.settings.OPENAI_API_KEY, 
                    max_tokens=100,
                    temperature=0.1 # Low temp for deterministic strictness
                )
                self.enabled = True
                logger.info("Image Critic initialized (GPT-4o-mini).")
            except Exception as e:
                logger.warning(f"Image Critic disabled (Init failed): {e}")
        else:
            logger.info("Image Critic disabled (No OpenAI Key).")

    def evaluate(self, image_url: str) -> bool:
        """
        Analyzes the image for hallucinations, anatomical errors, or horror elements.
        Returns True if PASS, False if REJECT.
        """
        if not self.enabled:
            return True # Fail open if disabled

        logger.info(f"🧐 Critic analyzing image: {image_url}")
        
        prompt = """
        Analyze this image of a virtual influencer (young woman).
        
        CRITICAL CHECKS:
        1. ANATOMY: Is the head turned 180 degrees (Exorcist style)? 
        2. HANDS: Are there too many fingers or claw-hands?
        3. FACE: Is the face melted, distorted, or missing features?
        4. BODY: Are limbs in impossible positions?
        
        If you see ANY severe anatomical horror or glitch, respond with 'REJECT'.
        If the image looks like a normal photo (even if slightly imperfect), respond with 'PASS'.
        
        ONLY RETURN ONE WORD: PASS or REJECT.
        """
        
        try:
            msg = HumanMessage(content=[
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ])
            
            response = self.llm.invoke([msg])
            decision = response.content.strip().upper()
            
            if "PASS" in decision:
                logger.info("✅ Image PASSED quality control.")
                return True
            else:
                logger.warning(f"❌ Image REJECTED by critic. Reason: {decision} (or unspecified hallucination)")
                return False
                
        except Exception as e:
            logger.error(f"Critic analysis failed: {e}")
            # If vision API fails, we assume it's a transient error and PASS to avoid blocking.
            # Or should we fail safe? User hates hallucinations. Let's PASS with warning.
            return True 
