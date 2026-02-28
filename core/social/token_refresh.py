# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

"""
Threads Token Auto-Renewal Module

The Threads API token expires after 60 days and cannot be made permanent.
This module automatically refreshes it before expiration (at 50 days),
updates the .env file so the new token persists across container restarts,
and updates the in-memory settings so no restart is needed.

Usage:
    Called automatically by the SmartScheduler once per day.
    Can also be run standalone:
        python -m core.social.token_refresh
"""

import json
import os
import re
import requests
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("Zirelia")

# Refresh when token is older than this many days (10-day safety margin before 60-day expiration)
REFRESH_THRESHOLD_DAYS = 50

# Path to the metadata file that tracks when the token was last refreshed
TOKEN_META_DIR = Path(os.getenv("TOKEN_META_DIR", "data"))
TOKEN_META_FILE = TOKEN_META_DIR / "threads_token_meta.json"

# Threads API endpoint for token refresh
REFRESH_URL = "https://graph.threads.net/refresh_access_token"


class ThreadsTokenRefresher:
    """
    Handles automatic renewal of the Threads API token.
    
    The refresh flow:
    1. Check token age from metadata file
    2. If >= REFRESH_THRESHOLD_DAYS, call Meta's refresh endpoint
    3. Update .env file with new token
    4. Update in-memory settings
    5. Save new timestamp to metadata file
    """

    def __init__(self):
        from config.settings import get_settings
        self.settings = get_settings()
        self.env_file = self._find_env_file()

    def check_and_refresh(self) -> dict:
        """
        Main entry point. Checks if the token needs refreshing and does so if needed.
        Returns a status dict with the result.
        """
        current_token = self.settings.THREADS_ACCESS_TOKEN
        
        if not current_token:
            logger.warning("🔑 Threads token not configured — skipping refresh check.")
            return {"status": "skipped", "reason": "no_token"}

        # Check token age
        age_days = self._get_token_age_days()
        
        if age_days is None:
            # First run — record current token timestamp but don't refresh yet
            logger.info("🔑 Threads token refresh: First run detected. Recording current timestamp.")
            self._save_token_meta(datetime.now(timezone.utc).isoformat())
            return {"status": "initialized", "message": "First run — timestamp recorded. Will refresh at 50 days."}

        logger.info(f"🔑 Threads token age: {age_days:.1f} days (refresh threshold: {REFRESH_THRESHOLD_DAYS} days)")

        if age_days < REFRESH_THRESHOLD_DAYS:
            days_until_refresh = REFRESH_THRESHOLD_DAYS - age_days
            logger.info(f"🔑 Token still fresh. Next refresh in ~{days_until_refresh:.0f} days.")
            return {"status": "skipped", "reason": "token_still_fresh", "age_days": age_days}

        # Token is old enough — refresh it
        logger.info(f"🔑 Token is {age_days:.0f} days old. Refreshing...")
        return self.refresh_token(current_token)

    def refresh_token(self, current_token: str) -> dict:
        """
        Calls the Threads API to refresh the token and updates all storage locations.
        """
        try:
            response = requests.get(REFRESH_URL, params={
                "grant_type": "th_refresh_token",
                "access_token": current_token
            }, timeout=30)

            data = response.json()

            if "access_token" not in data:
                error_msg = data.get("error", {}).get("message", str(data))
                logger.error(f"🔑 ❌ Token refresh failed: {error_msg}")
                return {"status": "error", "message": error_msg}

            new_token = data["access_token"]
            expires_in = data.get("expires_in", 5184000)  # Default 60 days in seconds

            logger.info(f"🔑 ✅ Token refreshed successfully! New expiry: {expires_in // 86400} days")

            # 1. Update .env file
            if self.env_file:
                self._update_env_file(new_token)
                logger.info(f"🔑 ✅ Updated {self.env_file} with new token")

            # 2. Update in-memory settings (bypass lru_cache)
            self.settings.THREADS_ACCESS_TOKEN = new_token

            # 3. Save refresh timestamp
            self._save_token_meta(datetime.now(timezone.utc).isoformat())
            logger.info("🔑 ✅ Token metadata saved")

            return {
                "status": "refreshed",
                "expires_in_days": expires_in // 86400,
                "token_preview": f"{new_token[:10]}...{new_token[-5:]}"
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"🔑 ❌ Network error during token refresh: {e}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            logger.error(f"🔑 ❌ Unexpected error during token refresh: {e}")
            return {"status": "error", "message": str(e)}

    def _get_token_age_days(self) -> float | None:
        """
        Returns the age of the current token in days, or None if no metadata exists.
        """
        if not TOKEN_META_FILE.exists():
            return None

        try:
            with open(TOKEN_META_FILE, "r") as f:
                meta = json.load(f)
            
            last_refresh = datetime.fromisoformat(meta["last_refresh"])
            # Ensure timezone awareness
            if last_refresh.tzinfo is None:
                last_refresh = last_refresh.replace(tzinfo=timezone.utc)
            
            age = datetime.now(timezone.utc) - last_refresh
            return age.total_seconds() / 86400  # Convert to days
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"🔑 Could not read token metadata: {e}")
            return None

    def _save_token_meta(self, refresh_timestamp: str):
        """
        Saves token refresh metadata to a JSON file.
        """
        TOKEN_META_DIR.mkdir(parents=True, exist_ok=True)
        
        meta = {
            "last_refresh": refresh_timestamp,
            "refresh_threshold_days": REFRESH_THRESHOLD_DAYS,
            "token_preview": f"{self.settings.THREADS_ACCESS_TOKEN[:10]}..." if self.settings.THREADS_ACCESS_TOKEN else None
        }

        with open(TOKEN_META_FILE, "w") as f:
            json.dump(meta, f, indent=2)

    def _update_env_file(self, new_token: str):
        """
        Updates the THREADS_ACCESS_TOKEN value in the .env file.
        Uses regex to find and replace the exact line.
        """
        if not self.env_file or not os.path.exists(self.env_file):
            logger.warning("🔑 .env file not found — cannot persist new token to disk.")
            return

        with open(self.env_file, "r") as f:
            content = f.read()

        # Replace the token value (handles both quoted and unquoted values)
        pattern = r'(THREADS_ACCESS_TOKEN\s*=\s*)["\']?[^"\'\n]*["\']?'
        replacement = f'THREADS_ACCESS_TOKEN="{new_token}"'
        
        new_content, count = re.subn(pattern, replacement, content)

        if count == 0:
            logger.warning("🔑 THREADS_ACCESS_TOKEN not found in .env — appending it.")
            new_content = content.rstrip() + f'\nTHREADS_ACCESS_TOKEN="{new_token}"\n'

        with open(self.env_file, "w") as f:
            f.write(new_content)

    def _find_env_file(self) -> str | None:
        """
        Locates the .env file relative to the project root.
        """
        # Try common locations
        candidates = [
            Path(".env"),
            Path("/app/.env"),  # Docker mount point
            Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / ".env",
        ]
        
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)
        
        logger.warning("🔑 .env file not found in any expected location.")
        return None


# --- Standalone execution for manual testing ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    refresher = ThreadsTokenRefresher()
    result = refresher.check_and_refresh()
    print(f"\nResult: {json.dumps(result, indent=2)}")
