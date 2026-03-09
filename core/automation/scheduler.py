# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license


import time
import random
import logging
import subprocess
import os
from datetime import datetime, timedelta

import pytz
import os

# Configuration
TIMEZONE = pytz.timezone("America/Los_Angeles")
# Load from .env, default to 1 if not set
MAX_DAILY_POSTS = int(os.getenv("MAX_DAILY_POSTS", 1))

# Simple Holiday Dictionary (Expandable via config later)
HOLIDAYS = {
    # Format: "MM-DD"
    "01-01": "New Year's Day, fresh start, resolutions",
    "02-14": "Valentine's Day, love, romance, self-love",
    "03-08": "International Women's Day, empowerment",
    "07-04": "Independence Day, fireworks, summer bbq",
    "10-31": "Halloween, spooky vibes, costume",
    "11-11": "Singles' Day / My Birthday! 🎉", # Personified!
    "11-28": "Thanksgiving, gratitude, food coma", # Varies yearly, manual update needed
    "12-25": "Christmas, cozy, gifts, family",
    "12-31": "New Year's Eve, party, reflection"
}

logger = logging.getLogger("Zirelia")

class SmartScheduler:
    def __init__(self):
        self.schedule = []
        self.today_str = ""
        self.posts_executed_today = 0

    def generate_daily_schedule(self):
        """
        Creates a randomized schedule for the current day.
        """
        # --- Threads Token Auto-Refresh (once per day) ---
        try:
            from core.social.token_refresh import ThreadsTokenRefresher
            refresher = ThreadsTokenRefresher()
            refresh_result = refresher.check_and_refresh()
            logger.info(f"🔑 Threads token check: {refresh_result.get('status', 'unknown')}")
        except Exception as e:
            logger.warning(f"🔑 Threads token refresh check failed (non-fatal): {e}")
        # -------------------------------------------------

        # maximize timezone correctness
        now = datetime.now(TIMEZONE)
        self.today_str = now.strftime("%Y-%m-%d")
        
        # 1. Check for Holiday
        month_day = now.strftime("%m-%d")
        holiday_context = HOLIDAYS.get(month_day, None)
        
        if holiday_context:
            logger.info(f"🎉 TODAY IS A SPECIAL DAY: {holiday_context}")
        
        # 2. Define Windows (Start Hour, End Hour, Label)
        # We always want at least one post if MAX_DAILY_POSTS >= 1
        windows = [
            (8, 10, "Morning_Routine"),   # Morning: 8am - 10am
            (13, 15, "Afternoon_Vibe"),   # Afternoon: 1pm - 3pm
            (19, 22, "Evening_Chill")     # Evening: 7pm - 10pm
        ]
        
        # Select purely random windows based on MAX_DAILY_POSTS limit
        # This ensures we don't always pick Morning if limit is 1.
        selected_windows = random.sample(windows, min(MAX_DAILY_POSTS, len(windows)))
        
        self.schedule = []
        for start_h, end_h, label in selected_windows:
            # Random minute
            hour = random.randint(start_h, end_h - 1)
            minute = random.randint(0, 59)
            
            # Create timezone-aware datetime
            post_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Use holiday topic if available, otherwise routine
            topic_override = holiday_context if holiday_context else None
            
            # Only schedule if time hasn't passed yet
            if post_time > now:
                self.schedule.append({
                    "time": post_time,
                    "label": label,
                    "topic": topic_override
                })
        
        # Sort by time
        self.schedule.sort(key=lambda x: x['time'])
        
        logger.info(f"📅 SCHEDULE FOR {self.today_str}:")
        for item in self.schedule:
            topic_str = f" (Topic: {item['topic']})" if item['topic'] else ""
            logger.info(f"   -> {item['time'].strftime('%H:%M')} [{item['label']}]{topic_str}")

    def run_loop(self):
        """
        Infinite loop that checks the schedule locally.
        """
        logger.info("🕰️ Smart Scheduler STARTED. Press Ctrl+C to stop.")
        
        while True:
            # New Day Check
            now_aware = datetime.now(TIMEZONE)
            current_day = now_aware.strftime("%Y-%m-%d")
            
            # New day: reset counter and regenerate schedule
            if self.today_str != current_day:
                self.posts_executed_today = 0
                self.generate_daily_schedule()
            # Same day but schedule empty: only regenerate if we haven't hit the limit
            elif not self.schedule and self.posts_executed_today < MAX_DAILY_POSTS:
                self.generate_daily_schedule()
            
            # Re-fetch now (in case schedule generation took time)
            now = datetime.now(TIMEZONE)
            next_post = None
            
            # Find next pending post
            for post in self.schedule:
                if post['time'] > now:
                    next_post = post
                    break
            
            if next_post:
                # Sleep until next post (or max 1 hour check)
                wait_seconds = (next_post['time'] - now).total_seconds()
                
                # If wait is long, sleep in chunks to allow graceful exit/date change check
                wait_hours = wait_seconds / 3600
                logger.info(f"💤 Sleeping until {next_post['time'].strftime('%H:%M')} (LA time) - approx {wait_hours:.1f} hours from now...")
                
                if wait_seconds > 300:
                    time.sleep(300) 
                    continue
                else:
                    logger.info(f"🚀 Launching post sequence in {int(wait_seconds)} seconds...")
                    time.sleep(wait_seconds)
                    
                    # EXECUTE POST
                    self._execute_post(next_post)
                    self.posts_executed_today += 1
                    
                    # Remove from schedule
                    self.schedule.remove(next_post)
                    
                    logger.info(f"📊 Posts executed today: {self.posts_executed_today}/{MAX_DAILY_POSTS}")
            else:
                # No more posts today
                logger.info("✅ All posts for today completed. Sleeping until tomorrow...")
                time.sleep(3600) # Sleep 1 hour

    def _execute_post(self, post):
        """
        Calls main.py to execute the actual posting logic.
        """
        logger.info(f"⚡ PREPARING SCHEDULED POST: {post['label']}")
        
        # Read active platforms from env or default to instagram
        active_platforms_env = os.getenv("ACTIVE_PLATFORMS", "instagram,facebook,threads")
        active_platforms = [p.strip() for p in active_platforms_env.split(",") if p.strip()]

        for platform in active_platforms:
            logger.info(f"⚡ EXECUTING SCHEDULED POST ON: {platform.upper()}")
            try:
                # Construct command
                cmd = ["python", "-u", "main.py", "--platform", platform]
                
                if post['topic']:
                    cmd.extend(["--topic", post['topic']])
                
                # We call main.py as a subprocess to ensure clean state for each run
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ Post executed successfully on {platform.upper()}.")
                    for line in result.stdout.splitlines():
                        logger.debug(line)
                else:
                    logger.error(f"❌ Post failed on {platform.upper()}:")
                    for line in result.stderr.splitlines():
                        logger.error(line)
                    
            except Exception as e:
                logger.error(f"❌ Execution error on {platform.upper()}: {e}")

if __name__ == "__main__":
    # Setup basic logging for standalone run
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    scheduler = SmartScheduler()
    scheduler.run_loop()
