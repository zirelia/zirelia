# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import os
import time
import requests
import replicate
from virtual_influencer_engine.config.settings import get_settings
from virtual_influencer_engine.core.utils.logger import logger

# Initialize Settings
settings = get_settings()

# Configuration
OUTPUT_DIR = "casting_sienna"
NUM_IMAGES = 10  # How many candidates to generate
MODEL = "black-forest-labs/flux-1.1-pro" # Top quality standard for casting

# The "Golden Prompt" for Sienna Fox (Visual Identity)
# Precise facial features to ensure we get High-Quality candidates
PROMPT = """
A hyper-realistic close-up portrait of a 25-year-old woman named Sienna Fox. 
She has dirty blonde messy wavy hair and expressive hazel eyes. 
She has a symmetric face, sun-kissed skin texture, natural freckles, and a small imperfection on her left eyebrow. 
Soft natural lighting, 85mm lens, f/1.8, cinematic depth of field, bokeh background.
Looking directly at the camera with a confident, slightly flirty smile.
High resolution, 8k, raw photo style, unedited.
"""

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    return False

def main():
    if not settings.REPLICATE_API_TOKEN:
        logger.error("REPLICATE_API_TOKEN is missing in .env")
        return

    ensure_dir(OUTPUT_DIR)
    logger.info(f"Starting Casting Session for Sienna Fox...")
    logger.info(f"Generating {NUM_IMAGES} candidates using FLUX.1 Pro...")

    client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)

    for i in range(1, NUM_IMAGES + 1):
        logger.info(f"Generating Candidate #{i}...")
        
        try:
            # Random seed is automatic if not specified
            output = client.run(
                MODEL,
                input={
                    "prompt": PROMPT,
                    "aspect_ratio": "1:1", # Portrait/Headshot shape
                    "output_format": "jpg",
                    "output_quality": 100,
                    "safety_tolerance": 2 # Allow some natural skin
                }
            )
            
            # FLUX 1.1 Pro returns a generic output, usually a string/url or stream
            image_url = str(output)
            
            filename = os.path.join(OUTPUT_DIR, f"sienna_candidate_{i:02d}.jpg")
            if download_image(image_url, filename):
                logger.info(f"SAVED: {filename}")
            else:
                logger.error(f"Failed to download image from {image_url}")

        except Exception as e:
            logger.error(f"Error generating candidate #{i}: {e}")
        
        # Avoid rate limits
        time.sleep(2)

    logger.info("Nodes generati! Controlla la cartella 'casting_sienna' e scegli la tua PREFERITA.")

if __name__ == "__main__":
    main()
