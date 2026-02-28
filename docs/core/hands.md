# The Hands (Social Integration)

The "Hands" module is responsible for publishing the generated content (text + image) to social media platforms.

## Supported Platforms

### Twitter / X ✅
We use the **Tweepy** library to interact with the Twitter API.
*   **Media Upload**: Images are uploaded first to get a `media_id`.
*   **Tweet Posting**: Text is posted with the attached `media_id`.
*   **Safety**: Includes random delays to mimic human behavior.

### Facebook ✅
Automated posting to a Facebook Page via Meta Graph API.
*   Uses a **Permanent Page Access Token** obtained through the extended token exchange flow.
*   Supports text-only and image + text posts (image must be a public URL).

### Instagram ✅
Automated posting to an Instagram Professional account via Meta Graph API.
*   **3-Step Process**: Create media container → Poll for processing → Publish.
*   Requires a public image URL (the Replicate output URL is used directly).
*   Always requires an image — text-only posts are not supported by the API.

### Threads ✅
Automated posting via the dedicated Threads API (`graph.threads.net`).

!!! important "Separate Meta App Required"
    Threads uses a **completely separate Meta App** from Facebook/Instagram. It has its own App ID, App Secret, and OAuth token. See the [Meta API Setup Guide](../guides/meta_setup.md) for details.

*   **Text-Only Ratio**: By default, ~70% of Threads posts are text-only (no image), controlled by `THREADS_TEXT_ONLY_RATIO`.
*   **Viral Strategy**: Threads prompts are optimized for engagement — hot takes, questions, relatable rants.
*   **Cross-Promo**: When a Threads post includes an image, the AI subtly hints at more content on Instagram.
*   **Auto Token Renewal**: Threads tokens expire every 60 days. The system automatically refreshes them at 50 days.

## Content Safety

The image generation pipeline includes a content moderation layer:

*   **No lingerie, underwear, or bikini** content is generated for any platform.
*   The visual prompt generator explicitly blocks revealing clothing descriptions.
*   Approved outfit categories: casual wear, athletic wear, streetwear, dresses, professional attire.

## Key Files
*   `core/social/twitter.py`: Twitter/X client (Tweepy).
*   `core/social/meta.py`: `MetaClient` (Facebook/Instagram) and `ThreadsClient` (Threads).
*   `core/social/platforms.py`: Platform managers and factory pattern.
*   `core/social/token_refresh.py`: Automatic Threads token renewal.
