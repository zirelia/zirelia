# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import time
import random
import os
from typing import Dict, Any, List

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("[Safety] Warning: Redis library not found. Falling back to in-memory storage.")

class SafetyManager:
    """
    Manages safety checks, rate limits, and anti-ban measures.
    Uses Redis for persistence across processes.
    """
    def __init__(self):
        # Default rate limits (posts per hour)
        self.rate_limits = {
            "twitter": 2,
            "instagram": 1,
            "facebook": 1,
            "threads": 2
        }

        # Connect to Redis
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.use_redis = False
        self.local_storage: Dict[str, float] = {}
        self.redis_client = None

        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
                self.use_redis = True
            except Exception as e:
                print(f"[Safety] Warning: Redis connection failed ({e}). Using in-memory storage.")
        else:
            print("[Safety] Redis not installed. Using in-memory storage.")

        # Blacklist of prohibited keywords (simplified for demo)
        self.content_blacklist = [
            "buy now", "click here", "free money", "crypto scheme",
            "xxx", "nsfw", "adult only"
        ]

    def _get_last_post_time(self, platform: str) -> float:
        if self.use_redis:
            try:
                val = self.redis_client.get(f"last_post_time:{platform}")
                return float(val) if val else 0.0
            except Exception:
                # Fallback if Redis fails mid-operation
                return 0.0
        else:
            return self.local_storage.get(platform, 0.0)

    def _set_last_post_time(self, platform: str, timestamp: float):
        if self.use_redis:
            try:
                self.redis_client.set(f"last_post_time:{platform}", str(timestamp))
            except Exception:
                pass
        else:
            self.local_storage[platform] = timestamp

    def check_rate_limit(self, platform: str) -> bool:
        """
        Checks if posting is allowed on the given platform based on rate limits.
        """
        if platform not in self.rate_limits:
            print(f"[Safety] Unknown platform '{platform}', proceeding with caution.")
            return True # Default allow if unknown, but log warning

        current_time = time.time()
        last_time = self._get_last_post_time(platform)

        # Calculate minimum interval in seconds
        min_interval = 3600 / self.rate_limits[platform]

        if current_time - last_time < min_interval:
            wait_time = min_interval - (current_time - last_time)
            print(f"[Safety] Rate limit hit for {platform}. Please wait {wait_time:.1f}s.")
            return False

        return True

    def record_action(self, platform: str):
        """Records the time of a successful action."""
        self._set_last_post_time(platform, time.time())

    def apply_human_delay(self, base_delay: int = 5):
        """
        Sleeps for a random duration to simulate human behavior.
        """
        delay = base_delay + random.uniform(1.0, 5.0)
        print(f"[Safety] Simulating human delay: {delay:.2f}s...")
        time.sleep(delay)

    def validate_content(self, content: str) -> bool:
        """
        Checks content against blacklist. Returns True if safe.
        """
        content_lower = content.lower()
        for keyword in self.content_blacklist:
            if keyword in content_lower:
                print(f"[Safety] Content validation failed. Found blocked keyword: '{keyword}'")
                return False
        return True
