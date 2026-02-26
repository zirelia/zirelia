# Threads Viral Strategy — Implementation Plan

## Goal
Make Threads a **growth engine** for Sienna Fox: spark conversations, go viral with hot takes, and funnel followers organically to Instagram and Facebook.

## Strategy Overview

| Element | Detail |
|---|---|
| **Content Mix** | ~70% text-only (conversational), ~30% image+text |
| **Tone** | Unfiltered hot takes, relatable questions, spicy opinions |
| **Hashtags** | 0 (Threads doesn't reward hashtag spam) |
| **Cross-promo** | Subtle IG teases ("full set on IG 😏"), never link-dump |
| **Posting Frequency** | Same as other platforms (controlled by `MAX_DAILY_POSTS`) |

---

## Proposed Changes

### 1. Text-Only Ratio for Threads

#### `main.py`

When `platform == "threads"`, decide randomly whether to skip image generation based on `THREADS_TEXT_ONLY_RATIO`:

```python
# Before image generation, check if Threads should go text-only
import random

if platform == "threads":
    text_only_ratio = float(os.getenv("THREADS_TEXT_ONLY_RATIO", "0.7"))
    if random.random() < text_only_ratio:
        logger.info("🧵 Threads: TEXT-ONLY mode (no image this time)")
        image_path = None  # Skip image for this platform
```

Since the scheduler calls `main.py` separately for each platform, this works cleanly without affecting other platforms.

#### `.env.template`

```
# Threads Content Strategy
# Ratio of text-only posts on Threads (0.0 = always image, 1.0 = always text-only)
THREADS_TEXT_ONLY_RATIO=0.7
```

---

### 2. Viral Prompt Templates for Threads

#### `templates.py`

Upgrade the Threads template to be explicitly viral:

```python
"threads": {
    "requirements": (
        "Write as if texting your group chat. Pick ONE of these viral formats randomly:\n"
        "- HOT TAKE: A bold, slightly controversial opinion ('unpopular opinion: ...')\n"
        "- THIS OR THAT: Give two options and ask which one ('gym at 6am or gym at 11pm?')\n"
        "- RELATABLE VENT: A funny complaint everyone relates to\n"
        "- THIRST TRAP TEASE: Hint at IG content without a link ('the full set is... somewhere 😏')\n"
        "- RANDOM THOUGHT: A late-night or shower thought\n"
        "Keep it under 300 characters. No hashtags. End with something that begs a reply."
    ),
    "emoji_count": "1-2",
    "hashtag_count": "0",
}
```

#### `brain.py`

Update the Threads platform instructions:

```python
elif p_lower == "threads":
    platform_instructions = (
        "You are posting on Threads. Your goal is MAXIMUM ENGAGEMENT.\n"
        "Write something that people MUST reply to. Use one of these formats:\n"
        "1) A hot take or unpopular opinion\n"
        "2) A 'this or that' question\n"
        "3) A relatable rant/complaint\n"
        "4) A mysterious tease about new IG content\n"
        "5) A random shower thought\n"
        "Rules: Under 300 chars. No hashtags. Casual slang. "
        "End with a hook that demands a reply. Never say 'check out my Instagram'."
    )
```

---

### 3. Threads-Specific Persona Config

#### `persona.yaml`

Add a `threads` section under `platforms:`:

```yaml
platforms:
  threads:
    style: "Unfiltered thoughts, group chat energy, bold opinions, engagement bait"
    hashtag_density: "None"
    cross_promo: "Occasional subtle teases pointing to Instagram content"
```

---

### 4. Cross-Promotion Logic (Subtle IG Teases)

#### `brain.py`

When Threads generates a post that has image content (the 30% image posts), append a subtle cross-promo hint:

```python
# In generate_thought(), when platform is threads and there's image context
if p_lower == "threads" and "Image Description" in context:
    platform_instructions += (
        "\nSince this post has a photo, subtly hint that more content "
        "is on your Instagram. Never use 'link in bio' or direct URLs. "
        "Example: '...the full set? you know where to find it 😏'"
    )
```

---

## Files Changed Summary

| File | Change |
|---|---|
| `main.py` | Text-only ratio logic for Threads |
| `.env.template` | `THREADS_TEXT_ONLY_RATIO` parameter |
| `templates.py` | Viral prompt formats |
| `brain.py` | Viral platform instructions + cross-promo hints |
| `persona.yaml` | Threads platform config section |

## Verification Plan

- Run `python main.py --platform threads --dry-run` multiple times (5-10x) to verify:
  - ~70% produce text-only output (no image generation call)
  - ~30% produce image + text
  - Captions are short, conversational, engagement-oriented
  - No hashtags appear
