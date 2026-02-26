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
    Client for Meta Graph API (Facebook, Instagram).
    Note: Threads uses a separate API — see ThreadsClient below.
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
        Step 2: Check Container Status
        Step 3: Publish Container
        """
        import time

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
        logger.info(f"Instagram: Created Media Container {container_id}. Waiting for processing...")

        # Step 2: Check Container Status (Polling)
        url_status = f"{self.BASE_URL}/{container_id}"
        payload_status = {
            "fields": "status_code",
            "access_token": self.access_token
        }
        
        # Wait up to 30 seconds for Meta to download and process the image from Replicate
        max_attempts = 6
        for attempt in range(max_attempts):
            time.sleep(5) # wait 5s between checks
            status_resp = self._make_request("GET", url_status, payload_status)
            status_code = status_resp.get("status_code", "ERROR")
            
            logger.info(f"Instagram: Container status: {status_code} (Attempt {attempt+1}/{max_attempts})")
            
            if status_code == "FINISHED":
                break
            elif status_code == "ERROR":
                return {"error": "Instagram failed to process the image container."}
            elif attempt == max_attempts - 1:
                logger.warning("Instagram: Container processing taking too long. Attempting to publish anyway...")

        # Step 3: Publish
        logger.info(f"Instagram: Publishing Media Container {container_id}...")
        url_publish = f"{self.BASE_URL}/{self.ig_account_id}/media_publish"
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


class ThreadsClient:
    """
    Client for the Threads API (graph.threads.net).
    Requires a SEPARATE Meta App created with the "Access the Threads API" use case,
    its own OAuth token, and a Threads User ID.
    Official docs: https://developers.facebook.com/docs/threads
    """
    BASE_URL = "https://graph.threads.net/v1.0"

    def __init__(self):
        self.access_token = settings.THREADS_ACCESS_TOKEN
        self.threads_user_id = settings.THREADS_USER_ID

        if not self.access_token:
            logger.warning("Threads Access Token missing. Threads posting will fail.")
        if not self.threads_user_id:
            logger.warning("Threads User ID missing. Threads posting will fail.")

    def post_threads(self, text: str, image_url: str = None) -> Dict[str, Any]:
        """
        Publishes to Threads.
        Step 1: Create Media Container
        Step 2: Publish Container
        """
        if not self.access_token or not self.threads_user_id:
            return {"error": "Threads credentials not configured (THREADS_ACCESS_TOKEN / THREADS_USER_ID)"}

        # Step 1: Create Container
        url_media = f"{self.BASE_URL}/{self.threads_user_id}/threads"
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
        logger.info(f"Threads: Created Media Container {container_id}")

        # Step 2: Publish
        url_publish = f"{self.BASE_URL}/{self.threads_user_id}/threads_publish"
        payload_publish = {
            "creation_id": container_id,
            "access_token": self.access_token
        }
        return self._make_request("POST", url_publish, payload_publish)

    def _make_request(self, method: str, url: str, params: Dict) -> Dict:
        try:
            if method == "POST":
                resp = requests.post(url, data=params)
            else:
                resp = requests.get(url, params=params)

            data = resp.json()
            if "error" in data:
                logger.error(f"Threads API Error: {data['error']}")
            return data
        except Exception as e:
            logger.error(f"Threads request failed: {e}")
            return {"error": str(e)}
