# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import argparse
import sys
import os
from config.settings import get_settings
from core.utils.logger import logger
from core.persona.engine import PersonaEngine
from core.content.generator import ContentGenerator
from core.image_gen.pipeline import ImageGenerator
from core.social.platforms import PlatformFactory

# Add current directory to path so virtual_influencer_engine can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

settings = get_settings()

# --- GLOBAL MONKEY PATCH FOR RASPBERRY PI PROXY ISSUES ---
import httpx
_original_client_init = httpx.Client.__init__
_original_async_client_init = httpx.AsyncClient.__init__

def patched_init(self, *args, **kwargs):
    # Remove unsupported arguments if they exist
    kwargs.pop('proxies', None)
    kwargs.pop('trust_env', None)
    _original_client_init(self, *args, **kwargs)

def patched_async_init(self, *args, **kwargs):
    # Remove unsupported arguments if they exist
    kwargs.pop('proxies', None)
    kwargs.pop('trust_env', None)
    _original_async_client_init(self, *args, **kwargs)

httpx.Client.__init__ = patched_init
httpx.AsyncClient.__init__ = patched_async_init
logger.warning("Applied global httpx.Client & AsyncClient monkey patch to ignore proxies")
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Zirelia CLI - Virtual Influencer Engine")
    
    # 1. Platform Selection
    parser.add_argument(
        "--platform", 
        type=str, 
        choices=["twitter", "instagram", "facebook", "threads", "all"],
        default="all",
        help="Select specific platform to post to."
    )
    
    # 2. Content Mode
    parser.add_argument(
        "--mode", 
        type=str, 
        choices=["hybrid", "text"],
        default="hybrid",
        help="Content mode: 'hybrid' (Text + Image) or 'text' (Text only)."
    )
    
    # 3. Topic (Optional - Auto Mode)
    parser.add_argument(
        "--topic", 
        type=str, 
        default=None,
        help="Context/Topic. Leave empty for Autonomous Mode (Random from Persona)."
    )
    
    # 4. Dry Run Flag (Testing Mode)
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Simulate execution without posting to social media."
    )

    args = parser.parse_args()

    logger.info(f"=== Starting {settings.PROJECT_NAME} ===")
    logger.info(f"Mode: {args.mode.upper()} | Platform: {args.platform.upper()} | Dry Run: {args.dry_run}")

    # Initialize Components
    config_path = os.path.join(os.getcwd(), "virtual_influencer_engine/config/persona.yaml")
    
    try:
        persona = PersonaEngine(config_path=config_path)
        content_gen = ContentGenerator(persona)
        image_gen = ImageGenerator()
    except Exception as e:
        logger.error(f"Failed to initialize engine components: {e}")
        return

    # Determine platforms
    platforms_to_run = []
    if args.platform == "all":
        # Run across all supported social platforms
        platforms_to_run = ["twitter", "instagram", "threads", "facebook"]
    else:
        platforms_to_run = [args.platform]

    try:
        # A. Determine Topic (Manual vs Auto) - ONCE FOR ALL PLATFORMS
        topic = args.topic
        if not topic:
            logger.info("No topic provided. Engaging Autonomous Mode...")
            topic = content_gen.get_autonomous_topic()
        
        logger.info(f"Selected Topic: {topic}")

        # B. Expand Visual Context (The Muse) - ONCE
        visual_context = content_gen.generate_visual_prompt(topic)
        logger.info(f"Visual Context: {visual_context}")

        # C. Generate Image - ONCE
        image_path = None
        if args.mode == "hybrid" or "instagram" in platforms_to_run:
            logger.info("Generating Main Image (Shared across platforms)...")
            image_path = image_gen.generate_image(visual_context, style="lifestyle")
            logger.info(f"Shared Image URL: {image_path}")

        # D. Iterate through platforms to generate specific copy and post
        for platform in platforms_to_run:
            logger.info(f"\n--- Processing {platform.upper()} ---")
            
            # E. Generate Text (Customized per platform)
            caption_context = f"Topic: {topic}"
            if args.mode == "text" and platform != "instagram":
                caption_context += " (Note: This is a text-only post, so focus on the copy.)"
                caption = content_gen.generate_caption(platform, caption_context)
            else:
                # Use visual context to write a caption that matches the image
                caption = content_gen.generate_caption(platform, visual_context)
            
            logger.info(f"Generated Caption for {platform.upper()}:\n{caption}")

            # F. Publish (or Dry Run)
            if args.dry_run:
                logger.info(f"🚫 DRY RUN: Skipping actual posting to {platform}.")
                logger.info(f"   [Draft] Text preview: {caption[:70]}...")
            else:
                logger.info(f"🚀 Publishing to {platform}...")
                manager = PlatformFactory.get_platform(platform, {})
                if manager:
                    # Platform specific check for missing image
                    if platform == "instagram" and not image_path:
                        logger.error("Instagram requires an image! Skipping.")
                        continue
                        
                    result = manager.post_content(caption, image_path)
                    logger.info(f"✅ Result: {result}")
                else:
                    logger.error(f"Platform manager for {platform} not found/implemented.")            
            
    except Exception as e:
        logger.error(f"Failed during multi-platform execution: {e}")

if __name__ == "__main__":
    main()
