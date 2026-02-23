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

from config.settings import get_settings

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger("EngagementLiker")

# Configuration (Safe Mode)
CHECK_INTERVAL_SECONDS = 3600 # 60 Minutes
MAX_LIKES_PER_RUN = 1
HISTORY_FILE = "engagement_likes.json"

# What to search for?
SEARCH_QUERIES = [
    "#DigitalArt -is:retweet -is:reply lang:en",
    "#VirtualInfluencer -is:retweet -is:reply lang:en",
    "#AIArtCommunity -is:retweet -is:reply lang:en",
]

class SmartLiker:
    def __init__(self):
        load_dotenv()
        self.settings = get_settings()
        self.client = self._init_twitter()
        self.my_id = self._get_my_id()
        self.liked_ids = self._load_history()

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
            json.dump(list(self.liked_ids), f)

    def run_once(self):
        if not self.client or not self.my_id:
            logger.error("Client not ready.")
            return

        # Pick one query
        import random
        query = random.choice(SEARCH_QUERIES)

        logger.info(f"🔍 Searching for: {query}")
        
        try:
            # Search Tweets
            response = self.client.search_recent_tweets(
                query=query,
                max_results=10, # Get more than needed to filter
                tweet_fields=['created_at', 'author_id', 'text']
            )

            if not response.data:
                logger.info("No tweets found.")
                return

            liked_count = 0
            
            for tweet in response.data:
                if str(tweet.id) in self.liked_ids:
                    continue # Already verified

                if tweet.author_id == self.my_id:
                     continue # Don't like own tweets

                if liked_count >= MAX_LIKES_PER_RUN:
                    logger.info("🛑 Max likes for this run reached. Stopping.")
                    break

                # Like Tweet
                logger.info(f"❤️ Liking tweet from User {tweet.author_id}: {tweet.text[:50]}...")
                
                try:
                    self.client.like(tweet.id)
                    logger.info(f"✅ Liked!")
                    
                    # Track
                    self.liked_ids.add(str(tweet.id))
                    self._save_history()
                    liked_count += 1
                    
                    time.sleep(15) 

                except Exception as e:
                    logger.error(f"❌ Failed to like: {e}")

        except Exception as e:
            logger.error(f"Error searching tweets: {e}")

    def loop(self):
        logger.info("🚀 Smart Liker STARTED (Safe Mode).")
        while True:
            self.run_once()
            logger.info(f"💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
            time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    bot = SmartLiker()
    bot.loop()
