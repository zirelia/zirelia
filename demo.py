# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from virtual_influencer_engine.config.settings import get_settings
from virtual_influencer_engine.core.utils.logger import logger
from virtual_influencer_engine.core.persona.engine import PersonaEngine
from virtual_influencer_engine.core.content.generator import ContentGenerator
from virtual_influencer_engine.core.image_gen.pipeline import ImageGenerator
from virtual_influencer_engine.core.social.platforms import PlatformFactory

# Load Settings
settings = get_settings()

def main():
    logger.info(f"=== Starting {settings.PROJECT_NAME} ({settings.ENV}) ===")
    
    # 1. Initialize Persona
    logger.info("1. Initializing Persona Engine...")
    config_path = os.path.join(os.getcwd(), "virtual_influencer_engine/config/persona.yaml")
    persona = PersonaEngine(config_path=config_path)
    logger.info(f"   Persona Loaded: {persona.get_personality_summary()}")

    # 2. Initialize Image Generator
    print("\n2. Initializing Image Generator...")
    image_gen = ImageGenerator()

    # 3. Initialize Content Generator
    print("\n3. Initializing Content Generator...")
    content_gen = ContentGenerator(persona)

    # 4. Generate Content for Twitter
    platform = "twitter"
    topic = "Morning coffee and coding"
    print(f"\n4. Generating content for {platform} about '{topic}'...")

    # Generate Image
    image_path = image_gen.generate_image(f"{topic}", style="lifestyle")
    print(f"   Image generated at: {image_path}")

    # Generate Caption
    caption = content_gen.generate_caption(platform, f"A photo of {topic}")
    print(f"   Caption generated: {caption}")

    # 5. Simulate Publishing
    print(f"\n5. Publishing to {platform}...")
    manager = PlatformFactory.get_platform(platform, {})
    result = manager.post_content(caption, image_path)
    print(f"   Result: {result}")

    # 6. Test Safety (Rate Limit)
    print(f"\n6. Testing Safety (Rate Limit)...")
    print(f"   Attempting immediate second post to {platform}...")
    result_fail = manager.post_content(caption, image_path)
    print(f"   Result: {result_fail}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
