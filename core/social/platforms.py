# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import random
from typing import Dict, Any
from .manager import SocialManager
from .meta import MetaClient
from .twitter import TwitterClient
from core.utils.logger import logger

class TwitterManager(SocialManager):
    def __init__(self, platform_name: str, config: Dict[str, Any]):
        super().__init__(platform_name, config)
        self.client = TwitterClient()

    def post_content(self, content: str, image_path: str = None) -> Dict[str, Any]:
        if not self.safety_manager.validate_content(content):
            return {"status": "error", "message": "Safety validation failed"}

        if not self.safety_manager.check_rate_limit("twitter"):
            return {"status": "error", "message": "Rate limit exceeded"}

        self.safety_manager.apply_human_delay()
        
        logger.info(f"[Twitter] Posting content...")
        result = self.client.post_tweet(content, image_path)
        
        if "error" not in result:
             self.safety_manager.record_action("twitter")
             
        return result

    def reply_to_comment(self, comment_id: str, text: str) -> Dict[str, Any]:
        # Implement reply logic using client...
        return {"status": "skipped", "message": "Not implemented yet"}

    def get_metrics(self) -> Dict[str, Any]:
        return {"status": "mock", "followers": 1200}

class MetaPlatformManager(SocialManager):
    """Base class for FB, IG, Threads sharing the Meta Client."""
    def __init__(self, platform_name: str, config: Dict[str, Any]):
        super().__init__(platform_name, config)
        self.client = MetaClient()

class InstagramManager(MetaPlatformManager):
    def post_content(self, content: str, image_path: str = None) -> Dict[str, Any]:
        if not image_path:
             return {"status": "error", "message": "Instagram requires an image"}
             
        if not self.safety_manager.validate_content(content):
            return {"status": "error", "message": "Safety validation failed"}

        if not self.safety_manager.check_rate_limit("instagram"):
             return {"status": "error", "message": "Rate limit exceeded"}

        logger.info(f"[Instagram] Posting content...")
        # Note: Meta Graph API for IG requires an image URL, not local path.
        # In a real deployed scenario, we'd need to upload the local image to a public S3 bucket first.
        # For now, we assume image_path might be a URL or fail.
        if not image_path.startswith("http"):
            logger.warning("Local image path provided. Instagram API requires public URL. Uploading mock...")
            return {"status": "error", "message": "Image must be a public URL"}
            
        result = self.client.post_instagram(content, image_path)
        
        if "error" not in result:
             self.safety_manager.record_action("instagram")
        return result

    def reply_to_comment(self, comment_id: str, text: str) -> Dict[str, Any]:
        return {"status": "skipped"}

    def get_metrics(self) -> Dict[str, Any]:
        return {"status": "mock"}

class FacebookManager(MetaPlatformManager):
    def post_content(self, content: str, image_path: str = None) -> Dict[str, Any]:
        if not self.safety_manager.validate_content(content):
            return {"status": "error", "message": "Safety validation failed"}
            
        if not self.safety_manager.check_rate_limit("facebook"):
             return {"status": "error", "message": "Rate limit exceeded"}

        logger.info(f"[Facebook] Posting content...")
        # Access token and page ID handled by MetaClient
        
        # Similar logic for image URL vs local path
        image_url = image_path if image_path and image_path.startswith("http") else None
        
        result = self.client.post_facebook(content, image_url)
        
        if "error" not in result:
             self.safety_manager.record_action("facebook")
        return result

    def reply_to_comment(self, comment_id: str, text: str) -> Dict[str, Any]:
        return {"status": "skipped", "message": "Not implemented yet"}

    def get_metrics(self) -> Dict[str, Any]:
        return {"status": "mock"}

class ThreadsManager(MetaPlatformManager):
    def post_content(self, content: str, image_path: str = None) -> Dict[str, Any]:
        if not self.safety_manager.validate_content(content):
             return {"status": "error", "message": "Safety validation failed"}
             
        if not self.safety_manager.check_rate_limit("threads"):
             return {"status": "error", "message": "Rate limit exceeded"}
             
        logger.info(f"[Threads] Posting content...")
        
        image_url = image_path if image_path and image_path.startswith("http") else None
        result = self.client.post_threads(content, image_url)
        
        if "error" not in result:
             self.safety_manager.record_action("threads")
        return result

    def reply_to_comment(self, comment_id: str, text: str) -> Dict[str, Any]:
         return {"status": "skipped"}

    def get_metrics(self) -> Dict[str, Any]:
        return {"status": "mock"}

class PlatformFactory:
    @staticmethod
    def get_platform(platform_name: str, config: Dict[str, Any]) -> SocialManager:
        if platform_name == "twitter":
            return TwitterManager(platform_name, config)
        elif platform_name == "instagram":
            return InstagramManager(platform_name, config)
        elif platform_name == "facebook":
            return FacebookManager(platform_name, config)
        elif platform_name == "threads":
            return ThreadsManager(platform_name, config)
        else:
            raise ValueError(f"Unknown platform: {platform_name}")
