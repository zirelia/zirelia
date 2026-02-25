# Configuration

Zirelia is configured via two main files:
1.  `.env` (Secrets & API Keys)
2.  `config/persona.yaml` (Personality, Behavior, Appearance)

---

## 🔐 Environment Variables (`.env`)

Create a `.env` file in the `virtual_influencer_engine` root directory.

### Core APIs
| Variable | Description | Required? |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | Used for the "Brain" (text generation). | ✅ Yes |
| `REPLICATE_API_TOKEN` | Used for the "Imagination" (image generation). | ✅ Yes |
| `REPLICATE_MODEL_VERSION` | The specific model version (e.g., FLUX.1 Pro or your Custom LoRA). | ✅ Yes |

### Twitter / X
| Variable | Description | Required? |
| :--- | :--- | :--- |
| `TWITTER_API_KEY` | Consumer Key from Developer Portal. | ✅ Yes |
| `TWITTER_API_SECRET` | Consumer Secret. | ✅ Yes |
| `TWITTER_ACCESS_TOKEN` | OAuth 1.0a Access Token (Read/Write). | ✅ Yes |
| `TWITTER_ACCESS_TOKEN_SECRET` | OAuth 1.0a Secret. | ✅ Yes |

### Meta (Facebook & Instagram)
| Variable | Description | Required? |
| :--- | :--- | :--- |
| `META_APP_ID` | Facebook Developer App ID. | 🔹 If using FB/IG |
| `META_APP_SECRET` | Facebook Developer App Secret. | 🔹 If using FB/IG |
| `META_ACCESS_TOKEN` | Permanent Page Access Token. | 🔹 If using FB/IG |
| `FACEBOOK_PAGE_ID` | The ID of the bridging Facebook Page. | 🔹 If using FB/IG |
| `INSTAGRAM_ACCOUNT_ID` | The ID of the linked Professional Instagram. | 🔹 If using Instagram |

### Threads
| Variable | Description | Required? |
| :--- | :--- | :--- |
| `THREADS_ACCESS_TOKEN` | Long-lived Threads API Token. | 🔹 If using Threads |
| `THREADS_USER_ID` | Threads User ID. | 🔹 If using Threads |

### Automation Settings
| Variable | Description | Default |
| :--- | :--- | :--- |
| `MAX_DAILY_POSTS` | Maximum posts per day (1-3). | `1` |

### Database & Redis (Docker handles these automatically)
| Variable | Description | Default (Docker) |
| :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL Connection String. | `postgresql://user:password@db:5432/influencer_db` |
| `REDIS_URL` | Redis Connection String. | `redis://redis:6379/0` |

---

## 🧠 Persona Configuration (`persona.yaml`)

This YAML file defines **who the bot is**. Editing this changes the bot's entire behavior without touching code.

Location: `virtual_influencer_engine/config/persona.yaml`

### Structure

```yaml
name: "Sienna Fox"
age: 23
nationality: "American (Los Angeles, CA)"

# Physical Appearance (Used by Image Generator)
physical_traits:
  hair: "Light Brown / Dirty Blonde (Wavy)"
  eyes: "Hazel / Warm Brown"
  body: "Slim-Thick / Hourglass / Athletic"
  vibe: "Natural, Sun-kissed"

# Psychological Traits (Used by Text Generator)
traits:
  - "Confident"
  - "Playful / Flirty"
  - "Witty"

# Voice & Tone
voice:
  tone: "Seductive but friendly"
  style: "Short, punchy, uses emojis naturally (✨, 😉)"

# Daily Routine (Used by Smart Scheduler)
routine:
  morning:
    - "Waking up in silk sheets"
    - "Morning stretch"
  afternoon:
    - "Working from a cafe"
    - "Gym workout"
  evening:
    - "Sunset at the beach"
    - "Glass of wine"
```

### How to update
1.  Edit the file.
2.  Restart the container: `docker compose restart api scheduler`
