# The Hands (Social Integration)

> [!IMPORTANT]
> **Current State (as of 2026-02-20):** Only **Twitter / X** is fully implemented and production-ready. Instagram and other platforms are planned but **not yet functional**. Running the bot on any platform other than Twitter will produce errors.

The "Hands" module is responsible for publishing the generated content (text + image) to social media platforms.

## Supported Platforms

### Twitter / X (Fully Automated)
We use the **Tweepy** library to interact with the Twitter API.
*   **Media Upload**: Images are uploaded first to get a `media_id`.
*   **Tweet Posting**: Text is posted with the attached `media_id`.
*   **Safety**: Includes random delays to mimic human behavior.

### Facebook & Instagram (Graph API)
**Status: 🔴 Not Implemented (Planned - Phase 4)**
The architecture supports Meta Graph API integration in the future.
*   **Facebook**: Page posting via Graph API using a Long-Lived Access Token.
*   **Instagram**: Automated posting via direct API if verified business account.

## Key Files
*   `core/social/twitter_client.py`: Handles OAuth and API calls.
*   `core/social/meta_client.py`: Adapter for Facebook/Instagram.
