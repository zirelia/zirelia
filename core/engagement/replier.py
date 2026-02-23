# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license


import os
import time
import json
import logging
import tweepy
from datetime import datetime
from dotenv import load_dotenv

from core.persona.brain import PersonaBrain
from config.settings import get_settings

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger("EngagementReplier")

# Configuration (Safe Mode)
CHECK_INTERVAL_SECONDS = 1800 # 30 Minutes
MAX_REPLIES_PER_RUN = 1
HISTORY_FILE = "engagement_replied.json"

class SmartReplier:
    def __init__(self):
        load_dotenv()
        self.settings = get_settings()
        self.brain = PersonaBrain() # Initialize persona for generating replies
        self.client = self._init_twitter()
        self.my_id = self._get_my_id()
        self.replied_ids = self._load_history()

    def _init_twitter(self):
        try:
            return tweepy.Client(
                consumer_key=self.settings.TWITTER_API_KEY,
                consumer_secret=self.settings.TWITTER_API_SECRET,
                access_token=self.settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=self.settings.TWITTER_ACCESS_TOKEN_SECRET,
                bearer_token=self.settings.TWITTER_BEARER_TOKEN
            )
        except Exception as e:
            logger.error(f"Failed to init Twitter Client: {e}")
            return None

    def _get_my_id(self):
        if not self.client: return None
        try:
            me = self.client.get_me()
            return me.data.id
        except Exception as e:
            logger.error(f"Could not fetch my own ID: {e}")
            return None

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    return set(json.load(f))
            except:
                return set()
        return set()

    def _save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(list(self.replied_ids), f)

    def run_once(self):
        if not self.client or not self.my_id:
            logger.error("Client not ready.")
            return

        logger.info("🔍 Checking for new mentions...")
        
        try:
            # Fetch mentions (expand fields to see author/text)
            response = self.client.get_users_mentions(
                id=self.my_id,
                max_results=5,
                tweet_fields=['created_at', 'author_id', 'text']
            )

            if not response.data:
                logger.info("No mentions found.")
                return

            reply_count = 0
            
            for tweet in response.data:
                if str(tweet.id) in self.replied_ids:
                    continue # Already handled

                if reply_count >= MAX_REPLIES_PER_RUN:
                    logger.info("🛑 Max replies for this run reached. Stopping.")
                    break

                # Generate Reply
                logger.info(f"💬 Found mention from User {tweet.author_id}: {tweet.text}")
                
                # Context for brain: "User said: [text]"
                context = f"A user mentioned me on Twitter saying: '{tweet.text}'"
                reply_text = self.brain.generate_thought(context, platform="twitter")
                
                # Clean up brain output (sometimes adds quotes)
                reply_text = reply_text.strip('"').strip("'")
                
                # Post Reply
                try:
                    self.client.create_tweet(
                        text=reply_text,
                        in_reply_to_tweet_id=tweet.id
                    )
                    logger.info(f"✅ Replied: {reply_text}")
                    
                    # Track
                    self.replied_ids.add(str(tweet.id))
                    self._save_history()
                    reply_count += 1
                    
                    # Sleep a bit between replies to be human
                    time.sleep(10) 

                except Exception as e:
                    logger.error(f"❌ Failed to reply: {e}")

        except Exception as e:
            logger.error(f"Error checking mentions: {e}")

    def loop(self):
        logger.info("🚀 Smart Replier STARTED (Safe Mode).")
        while True:
            self.run_once()
            logger.info(f"💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
            time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    bot = SmartReplier()
    bot.loop()
