# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license


import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from virtual_influencer_engine.core.persona.engine import PersonaEngine
from virtual_influencer_engine.core.content.generator import ContentGenerator
from virtual_influencer_engine.core.image_gen.pipeline import ImageGenerator
from virtual_influencer_engine.core.utils.logger import logger

# --- MONKEY PATCH FOR PROXY ISSUES (Same as main.py) ---
import httpx
def patched_init(self, *args, **kwargs):
    kwargs.pop('proxies', None)
    kwargs.pop('trust_env', None)
    httpx.Client.__init__ = httpx.Client.__init__ # Revert to avoid recursion if strictly needed, but here we just pass
    # Actually, simpler patch:
    # Just allow the script to run by ignoring proxy env vars globally for this process
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)

# -------------------------------------------------------

def simulate_cycle():
    print("\n🎬 STARTING SIMULATION: A Day in the Life of Sienna Fox 🎬")
    print("===========================================================")
    
    # 1. Setup Output Directory
    base_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "simulated_output"))
    os.makedirs(base_output_dir, exist_ok=True)
    
    # 2. Initialize Components
    print("[1/2] Waking up Brain...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(os.path.join(script_dir, "../config/persona.yaml"))
    
    if not os.path.exists(config_path):
        print(f"❌ Config not found at: {config_path}")
        return

    persona = PersonaEngine(config_path=config_path)
    content_gen = ContentGenerator(persona) 
    image_gen = ImageGenerator()
    
    # 3. Define Schedule
    schedule = [
        {"time": "08:00", "hour": 8, "label": "Morning_Routine"},
        {"time": "13:00", "hour": 13, "label": "Afternoon_Vibe"},
        {"time": "20:00", "hour": 20, "label": "Evening_Chill"}
    ]

    for slot in schedule:
        print(f"\n⏰ SIMULATING TIME: {slot['time']} ({slot['label']})")
        print("-" * 40)
        
        # Create sub-folder for this slot
        timestamp = datetime.now().strftime("%Y%m%d")
        slot_dir = os.path.join(base_output_dir, f"{timestamp}_{slot['label']}")
        os.makedirs(slot_dir, exist_ok=True)
        
        # A. Pick Topic (Forced Hour)
        topic = content_gen.get_autonomous_topic(forced_hour=slot['hour'])
        print(f"👉 Selected Topic: {topic}")
        
        # B. Generate Text
        platform = "instagram"
        print(f"📝 Writing caption for {platform}...")
        caption = content_gen.generate_caption(platform, f"Photo of Sienna doing {topic}", {"topic": topic, "time_of_day": slot['label']})
        
        # C. Generate Image
        print("📸 Taking the photo...")
        image_url = image_gen.generate_image(f"{topic}, candid, lifestyle", style="cinematic")
        
        # D. Save Results
        print("💾 Saving...")
        
        # Save Text
        text_path = os.path.join(slot_dir, "caption.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(f"TOPIC: {topic}\n")
            f.write(f"TIME: {slot['time']}\n")
            f.write("-" * 20 + "\n")
            f.write(caption)
        
        # Save Image
        image_path = os.path.join(slot_dir, "photo.jpg")
        
        if image_url and image_url.startswith("http"):
            import requests
            resp = requests.get(image_url)
            if resp.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(resp.content)
            else:
                print(f"❌ Failed to download image")
        
        print(f"✅ Saved to: {slot_dir}")

    print(f"\n✨ Full Day Simulation Complete! Check folder: {base_output_dir}")

if __name__ == "__main__":
    simulate_cycle()
