# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

from abc import ABC, abstractmethod
from typing import Dict, Any
from ..safety.manager import SafetyManager

class SocialManager(ABC):
    def __init__(self, platform_name: str, config: Dict[str, Any]):
        self.platform_name = platform_name
        self.config = config
        self.safety_manager = SafetyManager()

    @abstractmethod
    def post_content(self, content: str, image_path: str = None) -> Dict[str, Any]:
        """Posts content to the platform."""
        pass

    @abstractmethod
    def reply_to_comment(self, comment_id: str, text: str) -> Dict[str, Any]:
        """Replies to a specific comment."""
        pass

    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Retrieves metrics for the platform."""
        pass
