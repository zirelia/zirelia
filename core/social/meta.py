# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import requests
from typing import Dict, Any, Optional
from config.settings import get_settings
from core.utils.logger import logger

settings = get_settings()

class MetaClient:
    """
    Client for Meta Graph API (Facebook, Instagram, Threads).
    """
    BASE_URL = "https://graph.facebook.com/v18.0"

    def __init__(self):
        self.access_token = settings.META_ACCESS_TOKEN
        self.page_id = settings.FACEBOOK_PAGE_ID
        self.ig_account_id = settings.INSTAGRAM_ACCOUNT_ID
        
        if not self.access_token:
            logger.warning("Meta Access Token missing. Social posting will fail.")

    def post_facebook(self, message: str, image_url: str = None) -> Dict[str, Any]:
        """Publishes a post to the Facebook Page."""
        url = f"{self.BASE_URL}/{self.page_id}/feed"
        payload = {
            "message": message,
            "access_token": self.access_token
        }
        if image_url:
            url = f"{self.BASE_URL}/{self.page_id}/photos"
            payload["url"] = image_url
        
        return self._make_request("POST", url, payload)

    def post_instagram(self, caption: str, image_url: str) -> Dict[str, Any]:
        """
        Publishes a post to Instagram (Business).
        Step 1: Create Media Container
        Step 2: Publish Container
        """
        # Step 1: Create Container
        url_media = f"{self.BASE_URL}/{self.ig_account_id}/media"
        payload_media = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }
        response = self._make_request("POST", url_media, payload_media)
        if "id" not in response:
            return response # Error

        container_id = response["id"]

        # Step 2: Publish
        url_publish = f"{self.BASE_URL}/{self.ig_account_id}/media_publish"
        payload_publish = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        return self._make_request("POST", url_publish, payload_publish)

    def post_threads(self, text: str, image_url: str = None) -> Dict[str, Any]:
        """
        Publishes to Threads.
        Similar to IG: Create Container -> Publish.
        """
        # Step 1: Create Container
        url_media = f"{self.BASE_URL}/{self.ig_account_id}/threads" # Endpoint might differ slightly based on rollout
        # Note: Threads API is new. Using standard container pattern.
        payload_media = {
            "media_type": "TEXT" if not image_url else "IMAGE",
            "text": text,
            "access_token": self.access_token
        }
        if image_url:
            payload_media["image_url"] = image_url
            
        response = self._make_request("POST", url_media, payload_media)
        if "id" not in response:
            return response

        container_id = response["id"]

        # Step 2: Publish
        url_publish = f"{self.BASE_URL}/{self.ig_account_id}/threads_publish"
        payload_publish = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        return self._make_request("POST", url_publish, payload_publish)

    def _make_request(self, method: str, url: str, params: Dict) -> Dict:
        if not self.access_token:
             return {"error": "No Access Token"}
             
        try:
            if method == "POST":
                resp = requests.post(url, data=params)
            else:
                resp = requests.get(url, params=params)
            
            data = resp.json()
            if "error" in data:
                logger.error(f"Meta API Error: {data['error']}")
            return data
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return {"error": str(e)}
