# Safety & Anti-Ban Strategy

This document outlines the measures implemented to prevent account suspension, shadow-banning, and spam detection.

## 1. Rate Limiting
- **Platform-Specific Limits**: Each platform has a defined limit (e.g., 5 posts per day for Twitter, 2 for Instagram).
- **Time Window**: Checks if the last post was made within a specified time window (e.g., 1 hour).
- **Hard Limits**: Prevents excessive posting even if requested by the user.

## 2. Randomized Delays (Humanization)
- **Posting Delays**: Adds a random delay (e.g., 30-120 seconds) before posting to simulate human behavior.
- **Typing Delays**: Simulated delay based on the length of the content.
- **Scroll/Interaction Delays**: Simulates browsing behavior before posting.

## 3. Content Filtering
- **Keyword Blacklist**: Scans content for prohibited words (e.g., explicit content, hate speech, spam triggers).
- **Duplicate Detection**: Prevents posting the exact same content multiple times.
- **A/B Testing**: Rotates captions to avoid repetitive patterns.

## 4. Metadata Safety
- **EXIF Removal**: Strips metadata from generated images to avoid tracking.
- **Fingerprinting Avoidance**: Varies browser fingerprints (if using web automation).

## 5. Compliance
- **Platform Terms of Service**: The system is designed to adhere to the ToS of Twitter, Instagram, Facebook, and Threads.
- **User Agent Rotation**: Uses random user agents for API requests (if scraping is involved).

## 6. Implementation Details
The `SafetyManager` class (`core/safety/manager.py`) encapsulates these checks.
- `check_rate_limit(platform)`: Checks if posting is allowed.
- `apply_human_delay()`: Sleeps for a random duration.
- `validate_content(content)`: Checks against the blacklist.
