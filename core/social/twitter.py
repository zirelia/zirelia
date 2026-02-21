# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

from typing import Dict, Any, Optional
from virtual_influencer_engine.config.settings import get_settings
from virtual_influencer_engine.core.utils.logger import logger

settings = get_settings()

try:
    import tweepy
    TWEEPY_AVAILABLE = True
except ImportError:
    TWEEPY_AVAILABLE = False
    logger.warning("Tweepy not found. Twitter functionality disabled.")

class TwitterClient:
    def __init__(self):
        self.client_v1 = None
        self.client_v2 = None
        
        if not TWEEPY_AVAILABLE:
            return

        if not settings.TWITTER_API_KEY:
             logger.warning("Twitter API keys missing.")
             return

        try:
            # V2 Client for posting tweets
            self.client_v2 = tweepy.Client(
                consumer_key=settings.TWITTER_API_KEY,
                consumer_secret=settings.TWITTER_API_SECRET,
                access_token=settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
                bearer_token=settings.TWITTER_BEARER_TOKEN
            )
            
            # V1 Client for media upload (V2 doesn't support media upload yet)
            auth = tweepy.OAuth1UserHandler(
                settings.TWITTER_API_KEY,
                settings.TWITTER_API_SECRET,
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.client_v1 = tweepy.API(auth)
            
            logger.info("Twitter Clients (V1 & V2) initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {e}")

    def post_tweet(self, text: str, image_path: str = None) -> Dict[str, Any]:
        """Posts a tweet, optionally with an image (local path or URL)."""
        if not self.client_v2: 
            return {"error": "Client not initialized"}

        media_id = None
        temp_file = None

        try:
            if image_path:
                # Handle Remote URL
                if image_path.startswith("http"):
                    import requests
                    import tempfile
                    import os

                    logger.info(f"Downloading image from {image_path}...")
                    response = requests.get(image_path, stream=True)
                    response.raise_for_status()

                    # Create temp file
                    fd, temp_file_path = tempfile.mkstemp(suffix=".jpg")
                    os.close(fd) # Close file descriptor, we'll open via path
                    
                    with open(temp_file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192): 
                            f.write(chunk)
                    
                    image_path = temp_file_path
                    temp_file = temp_file_path # Mark for deletion

                if self.client_v1:
                    # Upload media using V1.1 API
                    logger.info(f"Uploading media: {image_path}")
                    media = self.client_v1.media_upload(filename=image_path)
                    media_id = media.media_id
            
            # Post tweet using V2 API
            response = self.client_v2.create_tweet(
                text=text,
                media_ids=[media_id] if media_id else None
            )
            
            logger.info(f"Tweet posted successfully! ID: {response.data['id']}")
            return {"id": response.data['id'], "text": response.data['text']}

        except Exception as e:
            logger.error(f"Failed to post tweet: {e}")
            return {"error": str(e)}
        finally:
            # Cleanup temp file if created
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logger.debug(f"Removed temp file: {temp_file}")
                except Exception as e:
                    logger.warning(f"Failed to remove temp file: {e}")
