# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import os
import time
import replicate
from openai import OpenAI
from config.settings import get_settings
from core.utils.logger import logger
from core.image_gen.critic import ImageCritic

settings = get_settings()

class ImageGenerator:
    def __init__(self):
        # 1. Check for Replicate (Priority for Consistency)
        if settings.REPLICATE_API_TOKEN:
            self.provider = "replicate"
            self.client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
            # Use model from settings.
            # RECOMMENDED FOR HIGH QUALITY: "lucataco/flux-dev-lora:..." or "ostris/flux-dev-lora-trainer:..."
            self.model = settings.REPLICATE_MODEL_VERSION
        
        # 2. Fallback to DALL-E 3
        elif settings.OPENAI_API_KEY and "dummy" not in settings.OPENAI_API_KEY:
            self.provider = "dall-e-3"
            import httpx
            self.client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                http_client=httpx.Client() # Fix for proxy issues on RPi
            )
        
        else:
            self.provider = "mock"
            self.client = None
            
        # Initialize Critic
        self.critic = ImageCritic()
        
        logger.info(f"ImageGenerator initialized with provider: {self.provider}")

    def _optimize_prompt_for_safety(self, prompt: str) -> str:
        """
        Injects modifiers to avoid known AI failure modes (like hands).
        """
        p_lower = prompt.lower()
        
        # 1. Hands / Holding Objects (Coffee, Tea, Cups)
        if any(w in p_lower for w in ["coffee", "tea", "cup", "latte", "mug", "drink"]):
            # Strategy: Favor compositions where hands are less prominent or simpler
            import random
            strategy = random.choice([
                "cup resting on table next to her",  # No hands (Safest)
                "holding cup with both hands, detailed fingers, anatomical hands", # Explicit quality call
                "drinking from cup, close up face, hands out of frame", # Hiding hands
                "hands resting on lap, cup on the table" # Separation
            ])
            logger.info(f"🛡️ Safety Injection (Hands): Adding '{strategy}'")
            prompt += f", {strategy}"

        return prompt

    def generate_image(self, prompt: str, style: str = "cinematic", aspect_ratio: str = "9:16") -> str:
        """
        Generates an image using Replicate (FLUX/SDXL) or DALL-E 3.
        Includes a Quality Control Loop (max 3 attempts).
        """
        # Optimize prompt BEFORE generation to save money
        prompt = self._optimize_prompt_for_safety(prompt)
        
        logger.info(f"Generating image with prompt: '{prompt}'")
        
        if self.provider == "mock":
             return "https://via.placeholder.com/1024x1792.png?text=Mock+Image"

        max_attempts = 3
        
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(f"🎨 Generating Image (Attempt {attempt}/{max_attempts})...")
                image_url = None

                if self.provider == "replicate":
                    # Check if it's a FLUX model (heuristic based on name or common usage)
                    is_flux = "flux" in self.model.lower()
                    
                    if is_flux:
                        # FLUX Custom LoRA Logic
                        full_prompt = prompt
                        if "black-forest-labs/flux-1.1-pro" not in self.model: 
                            # It's a custom LoRA (e.g. ostris/flux-dev-lora-trainer)
                            if "TOK" not in full_prompt:
                                full_prompt = f"photo of TOK, a young woman, {full_prompt}"
                        
                        # Add cinematic style modifiers
                        import random
                        lighting = random.choice([
                            "soft natural lighting", "warm golden hour light", 
                            "dramatic cinematic lighting", "soft window light",
                            "studio lighting with rim light"
                        ])
                        camera = "shot on 35mm film, f/1.8, depth of field, bokeh"
                        texture = "slight film grain, skin texture, raw photo, unedited"
                        
                        full_prompt += f", {lighting}, {camera}, {texture}, hyperrealistic, 8k"
                        
                        input_params = {
                            "prompt": full_prompt,
                            "aspect_ratio": aspect_ratio, 
                            "output_format": "jpg",
                            "output_quality": 95, 
                            "lora_scale": 0.95, 
                            "num_outputs": 1,
                            "disable_safety_checker": True,
                            "extra_lora_scale": 0.95 
                        }
                        
                        output = self.client.run(self.model, input=input_params)
                        
                        # Replicate output handling
                        if isinstance(output, list) and len(output) > 0:
                            image_url = str(output[0])
                        elif hasattr(output, '__iter__') and not isinstance(output, str):
                            for item in output:
                                image_url = str(item)
                                break
                        else:
                            image_url = str(output)

                    else:
                        # SDXL Logic (Legacy)
                        full_prompt = f"photo of TOK, {prompt}, {style} style, 8k, photorealistic"
                        
                        output = self.client.run(
                            self.model,
                            input={
                                "prompt": full_prompt,
                                "negative_prompt": "blurry, low quality, deformed, ugly, bad anatomy, extra fingers",
                                "width": 1024,
                                "height": 1792 if aspect_ratio == "9:16" else 1024,
                                "num_outputs": 1
                            }
                        )
                        image_url = str(output[0]) if isinstance(output, list) else str(output)
            
                elif self.provider == "dall-e-3":
                    # DALL-E 3 Logic
                    full_prompt = f"{style} style. {prompt}. High quality, detailed."
                    size = "1024x1792" if aspect_ratio == "9:16" else "1024x1024"
                    
                    response = self.client.images.generate(
                        model="dall-e-3",
                        prompt=full_prompt,
                        size=size,
                        quality="standard",
                        n=1,
                    )
                    image_url = response.data[0].url

                # --- CRITIC CHECK ---
                if image_url:
                    if self.critic.evaluate(image_url):
                        return image_url
                    else:
                        logger.warning(f"⚠️ Attempt {attempt} failed quality check. Waiting 3 minutes before retrying...")
                        if attempt < max_attempts:
                            time.sleep(180)
                        continue
                else:
                    logger.error(f"Attempt {attempt} produced no URL.")
            
            except Exception as e:
                logger.error(f"Image generation failed ({self.provider}, Attempt {attempt}): {e}")
                if attempt < max_attempts:
                    logger.info("Waiting 3 minutes before retrying...")
                    time.sleep(180)

        # If loop finishes without return
        logger.error("❌ All image generation attempts failed or were rejected.")
        return "error_generating_image"
