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
OUTPUT_DIR = "dataset_sienna"
MODEL = "black-forest-labs/flux-1.1-pro"

# 1. THE GOLDEN FACE PROMPT (The "Soul" of Sienna)
# This part MUST be identical in every prompt to maintain facial consistency.
# Note: Removed "close-up portrait" and "confident, slightly flirty smile" because those vary.
BASE_APPEARANCE = """
A hyper-realistic photo of a 25-year-old woman named Sienna Fox with dirty blonde messy wavy hair and expressive hazel eyes. 
She has a symmetric face, sun-kissed skin texture, natural freckles, and a small imperfection on her left eyebrow.
"""

# 2. VARIATIONS (Expressions, Body, Lighting)
# We need a mix of everything to train a robust LoRA.
# Format: (Filename Suffix, Prompt Addition)
VARIATIONS = [
    # --- EXPRESSIONS (Close-ups) ---
    ("face_smile", "Close-up portrait, looking at camera, warm inviting smile, natural lighting, bokeh background"),
    ("face_laugh", "Close-up portrait, laughing naturally, eyes slightly closed, candid moment, soft sunlight"),
    ("face_serious", "Close-up portrait, serious expression, intense gaze, dramatic lighting, studio background"),
    ("face_neutral", "Close-up portrait, neutral expression, calm look, passport photo style, white background"),
    ("face_side", "Side profile portrait, looking away, thoughtful expression, golden hour lighting"),
    
    # --- BODY & POSES (Waist-up / 3/4) ---
    ("body_arms_crossed", "Waist-up shot, wearing a simple white t-shirt, arms crossed, confident pose, standing in a modern living room"),
    ("body_coffee", "Waist-up shot, holding a coffee cup, wearing a cozy oversized sweater, sitting in a cafe, morning light"),
    ("body_selfie", "Mirror selfie shot, holding phone, wearing activewear, gym background, slightly messy hair"),
    
    # --- FULL BODY (Action / Context) ---
    ("full_walking", "Full body shot, walking on a city street, wearing jeans and leather jacket, motion blur, daytime"),
    ("full_sitting", "Full body shot, sitting on a park bench, reading a book, wearing a sundress, relaxed pose"),
    ("full_glam", "Full body shot, wearing an elegant evening dress, standing on a balcony, night city lights background"),
    
    # --- LIGHTING EXPERIMENTS ---
    ("light_golden", "Portrait shot, golden hour sunlight hitting the face, lens flare, dreamy atmosphere"),
    ("light_neon", "Portrait shot, neon blue and pink lighting, night club atmosphere, edgy look"),
    
    # --- ADDITIONAL EXPRESSIONS (Added for Nuance) ---
    ("face_surprised", "Close-up portrait, surprised expression, mouth slightly open, eyes wide, candid shot"),
    ("face_angry", "Close-up portrait, angry expression, frowning, intense stare, dramatic shadows"),
    ("face_tired", "Close-up portrait, tired expression, no makeup, messy bun, morning light, authentic look"),
    
    # --- ADDITIONAL BODY/ACTION ---
    
    # --- PROVOCATIVE / BODY FOCUSED (Added for Social Impact) ---
    ("body_rear_leggings", "Full body shot from behind, looking back over shoulder, wearing tight grey yoga leggings and sports bra, highlighting physique, gym setting"),
    ("body_bikini_rear", "Full body shot from behind, standing on a beach, wearing a brazilian bikini, sun-kissed skin, golden hour"),
    ("body_glam_dress", "Waist-up shot, wearing a deep red evening gown with low neckline, confident and alluring expression, luxury hotel lobby background"),
    ("body_casual_shorts", "Full body shot, walking away from camera, wearing denim shorts and crop top, city street background"),
    
    # --- MORE REAR VIEW / GLUTES FOCUS (Added per request) ---
    ("body_stairs_rear", "Full body shot from behind, walking up stairs, wearing tight jeans, highlighting curves, urban setting"),
    ("body_pool_edge", "Full body shot from behind, sitting on the edge of a pool, wearing a bikini, wet skin, summer vibes"),
    # --- MORE REAR VIEW / GLUTES FOCUS (Added per request) ---
    ("body_stairs_rear", "Full body shot from behind, walking up stairs, wearing tight jeans, highlighting curves, urban setting"),
    ("body_pool_edge", "Full body shot from behind, sitting on the edge of a pool, wearing a bikini, wet skin, summer vibes"),
    ("body_mirror_rear", "Mirror selfie from behind, looking back over shoulder, wearing elegant silk bodysuit, soft lighting, bedroom background"),
    
    # --- EXTRA BODY FOCUS (Chest & Glutes - Safe for Work) ---
    ("body_tight_dress_rear", "Full body shot from behind, walking away, wearing tight midi dress, accentuating hourglass figure and curves, high heels"),
    ("body_fitness_rear_squat", "Full body shot from behind, performing a squat, wearing seamless leggings and sports bra, gym setting, athletic physique"),
    ("body_corset_front", "Waist-up self-portrait, wearing a vintage corset top with sweetheart neckline, soft skin texture, romantic lighting"),
    ("body_bikini_laying_stomach", "Full body shot, lying on stomach on a towel at the beach, sunbathing, wearing bikini, shot from low angle"),
    # --- PLAYFUL / ALLURING (Added for Personality) ---
    ("face_biting_lip", "Close-up portrait, biting lower lip, flirtatious expression, looking directly at camera, soft focus"),
    ("face_finger_lips", "Close-up portrait, index finger resting gently on lips, thoughtful and playful expression, head tilted slightly"),
    ("body_hands_hips_rear", "Full body shot from behind, hands on hips, looking back over shoulder, wearing tight jeans and crop top, confident pose"),
    ("body_hand_collarbone", "Portrait shot, hand resting gently on collarbone near chest, soft expression, wearing a tank top, natural lighting"),
]

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
    logger.info(f"Starting Dataset Generation for Sienna Fox...")
    logger.info(f"Generating {len(VARIATIONS)} varied images using FLUX.1 Pro...")

    client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)

    for i, (suffix, variation_prompt) in enumerate(VARIATIONS, 1):
        filename = os.path.join(OUTPUT_DIR, f"sienna_{i:02d}_{suffix}.jpg")
        
        # Check if already exists to avoid re-generating
        if os.path.exists(filename):
            logger.info(f"Skipping {filename} (already exists)")
            continue

        # COMBINE: Base Appearance + Variation
        full_prompt = f"{variation_prompt}. {BASE_APPEARANCE} High resolution, 8k, raw photo style, unedited."
        
        # RETRY LOGIC for Rate Limits
        for attempt in range(3):
            try:
                logger.info(f"Generating #{i}: {suffix} (Attempt {attempt+1})...")
                logger.debug(f"Prompt: {full_prompt}")
                
                output = client.run(
                    MODEL,
                    input={
                        "prompt": full_prompt,
                        "aspect_ratio": "1:1" if "face" in suffix else "3:4", 
                        "output_format": "jpg",
                        "output_quality": 100,
                        "safety_tolerance": 2
                    }
                )
                
                image_url = str(output)
                if download_image(image_url, filename):
                    logger.info(f"SAVED: {filename}")
                    break # Success! Exit retry loop
                else:
                    logger.error(f"Failed to download image from {image_url}")
                    break # Don't retry download errors, only generation errors

            except Exception as e:
                logger.error(f"Error generating #{i} (Attempt {attempt+1}): {e}")
                
                if "429" in str(e) and attempt < 2:
                    wait_time = 30 * (attempt + 1) # Wait 30s, then 60s
                    logger.warning(f"Rate limit hit. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    break # Other errors or max retries reached
        
        # Avoid rate limits between successful generations
        time.sleep(5)

    logger.info("Dataset Generation Complete! Check 'dataset_sienna' folder.")
    logger.info("Review images -> Delete bad ones -> Zip the good ones -> Train LoRA.")

if __name__ == "__main__":
    main()
