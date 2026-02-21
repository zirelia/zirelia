# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license


import os
import sys

# Add project root to path (Zirelia/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from virtual_influencer_engine.core.image_gen.pipeline import ImageGenerator
from virtual_influencer_engine.config.settings import get_settings

def test_lora():
    print("Testing LoRA Generation...")
    settings = get_settings()
    print(f"Model ID: {settings.REPLICATE_MODEL_VERSION}")
    
    if "antoniotrento" not in settings.REPLICATE_MODEL_VERSION:
        print("WARNING: Model ID does not look like a custom LoRA!")
    
    generator = ImageGenerator()
    
    prompt = "close-up portrait of a beautiful young woman, smiling directly at camera, wearing casual white t-shirt, cafe background"
    print(f"Prompt: {prompt}")
    
    try:
        url = generator.generate_image(prompt, aspect_ratio="3:4")
        print(f"SUCCESS! Image URL: {url}")
        
        # Download the image
        import requests
        response = requests.get(url)
        if response.status_code == 200:
            output_path = "test_sienna.jpg"
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Saved to: {os.path.abspath(output_path)}")
        else:
            print("Failed to download image.")
            
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_lora()
