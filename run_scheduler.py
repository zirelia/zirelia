# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license


from virtual_influencer_engine.core.automation.scheduler import SmartScheduler
import logging
import sys
import os

# Ensure the correct path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure Logging
logger = logging.getLogger("Zirelia")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    logger.info("🤖 Starting Zirelia Smart Scheduler...")
    try:
        scheduler = SmartScheduler()
        scheduler.run_loop()
    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user.")
    except Exception as e:
        logger.error(f"❌ Fatal Scheduler Error: {e}") 
