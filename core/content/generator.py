# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import json
from typing import Dict, Any
from virtual_influencer_engine.core.content.workflow import ContentWorkflow
from virtual_influencer_engine.core.utils.logger import logger

class ContentGenerator:
    def __init__(self, persona_engine=None):
        # We ignore persona_engine here as the workflow instantiates its own brain
        # This keeps the API compatible with demo.py but switches to the new brain
        self.workflow = ContentWorkflow()
        logger.info("ContentGenerator initialized with LangGraph Workflow.")

    def generate_caption(self, platform: str, image_description: str, context: Dict[str, Any] = None) -> str:
        """
        Generates a caption using the LangGraph workflow.
        """
        full_context = f"Image Description: {image_description}\nContext: {context or {}}"
        
        logger.info(f"Starting content generation for {platform}...")
        try:
            result = self.workflow.run(platform, full_context)
            
            # Extract final draft from state
            final_draft = result.get('draft', "Error: No draft generated.")
            return final_draft
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return "Error generating content."

    def get_autonomous_topic(self, forced_hour: int = None) -> str:
        """
        Picks a topic based on time of day (Routine) and persona interests.
        This creates a realistic 'Day in the Life' cycle.
        """
        import random
        from datetime import datetime
        
        # 1. Determine Time of Day
        current_hour = forced_hour if forced_hour is not None else datetime.now().hour
        
        time_slot = "night" # Default
        if 6 <= current_hour < 12:
            time_slot = "morning"
        elif 12 <= current_hour < 18:
            time_slot = "afternoon"
        elif 18 <= current_hour < 23:
            time_slot = "evening"
            
        logger.info(f"Autonomous Mode: Time is {current_hour}:00 ({time_slot.upper()})")

        # 2. Fetch Options from Config
        config = self.workflow.brain.config
        routine = config.get("routine", {})
        interests = config.get("interests", [])
        
        # 3. Decision Logic: 70% Routine, 30% Random Interest
        # This keeps it grounded in reality but adds variety
        if routine.get(time_slot) and random.random() < 0.7:
            topic = random.choice(routine[time_slot])
            logger.info(f"Selected ROUTINE topic: '{topic}'")
        else:
            topic = random.choice(interests)
            logger.info(f"Selected INTEREST topic: '{topic}'")
            
        return topic

    def optimize_hashtags(self, platform: str, caption: str) -> str:
        # Optimization is now part of the 'drafter' node in the workflow normally.
        # Keeping this for interface compatibility.
        return caption

    def generate_visual_prompt(self, topic: str) -> str:
        """
        Wrapper to call the brain's visual prompt expander.
        """
        return self.workflow.brain.generate_visual_prompt(topic)
