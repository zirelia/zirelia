# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import argparse
import sys
import os
from virtual_influencer_engine.config.settings import get_settings
from virtual_influencer_engine.core.utils.logger import logger
from virtual_influencer_engine.core.persona.engine import PersonaEngine
from virtual_influencer_engine.core.content.generator import ContentGenerator
from virtual_influencer_engine.core.image_gen.pipeline import ImageGenerator
from virtual_influencer_engine.core.social.platforms import PlatformFactory

# Add current directory to path if needed
sys.path.append(os.getcwd())

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
        # In a real app, this list would come from config
        # Default to Twitter as it's the only one implemented fully
        platforms_to_run = ["twitter"]
    else:
        platforms_to_run = [args.platform]

    for platform in platforms_to_run:
        try:
            logger.info(f"\n--- Processing {platform.upper()} ---")
            
            # A. Determine Topic (Manual vs Auto)
            topic = args.topic
            if not topic:
                logger.info("No topic provided. Engaging Autonomous Mode...")
                topic = content_gen.get_autonomous_topic()
            
            logger.info(f"Selected Topic: {topic}")

            # B. Expand Visual Context (The Muse)
            # We generate a rich visual description first, so both text and image are aligned.
            visual_context = content_gen.generate_visual_prompt(topic)
            logger.info(f"Visual Context: {visual_context}")

            # C. Generate Text
            # We pass the visual context so the caption describes the scene accurately.
            caption_context = f"Topic: {topic}"
            if args.mode == "text":
                caption_context += " (Note: This is a text-only post, so focus on the copy.)"
                caption = content_gen.generate_caption(platform, caption_context)
            else:
                # In hybrid mode, we use the visual description as the primary context
                caption = content_gen.generate_caption(platform, visual_context)
            
            logger.info(f"Generated Caption: {caption}")

            # D. Generate Image
            image_path = None
            if args.mode == "hybrid":
                logger.info("Generating Image...")
                # Use the expanded visual prompt for variety
                image_path = image_gen.generate_image(visual_context, style="lifestyle")
                logger.info(f"Image URL: {image_path}")
            
            elif platform == "instagram" and args.mode == "text":
                logger.warning("Instagram requires an image! Switching to Hybrid mode for this platform.")
                image_path = image_gen.generate_image(visual_context, style="lifestyle")
                logger.info(f"Image URL: {image_path}")

            # E. Publish (or Dry Run)
            if args.dry_run:
                logger.info(f"🚫 DRY RUN: Skipping actual posting to {platform}.")
                logger.info(f"   [Draft] Text: {caption[:50]}...")
                logger.info(f"   [Draft] Image: {image_path}")
            else:
                logger.info(f"🚀 Publishing to {platform}...")
                manager = PlatformFactory.get_platform(platform, {})
                if manager:
                    result = manager.post_content(caption, image_path)
                    logger.info(f"✅ Result: {result}")
                else:
                    logger.error(f"Platform manager for {platform} not found/implemented.")            
        except Exception as e:
            logger.error(f"Failed to process {platform}: {e}")

if __name__ == "__main__":
    main()
