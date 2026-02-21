<div align="center">

# 🧜‍♀️ Zirelia

**Autonomous AI Virtual Influencer Engine**

[![License: ELv2](https://img.shields.io/badge/License-ELv2-purple.svg)](https://www.elastic.co/licensing/elastic-license)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![MkDocs](https://img.shields.io/badge/Docs-MkDocs%20Material-teal)](https://zirelia.github.io/zirelia/)
[![Platform](https://img.shields.io/badge/Platform-Twitter%20%2F%20X-black?logo=x)](https://x.com)

> A modular, self-running engine that creates, manages, and grows a virtual influencer persona — from generating thoughts and faces to posting autonomously on social media, 24/7.

**[📚 Full Documentation](https://zirelia.github.io/zirelia/)** · **[🚀 Quick Start](#-quick-start)** · **[🗺️ Roadmap](#️-roadmap)**

</div>

---

## ⚠️ Important — Read Before Starting

> **New account?** Starting the bot without a proper warm-up is the #1 cause of permanent shadowbans.
> 👉 **[Read the Account Warm-Up & Anti-Ban Guide first.](https://zirelia.github.io/zirelia/guides/account_warmup/)**

---

## 🧠 What is Zirelia?

Zirelia is a **fully autonomous virtual influencer engine**. You define a personality in a YAML file — the engine does the rest:

1. **Thinks** — An LLM brain (OpenAI GPT-4) generates contextual, on-brand thoughts based on the persona's daily routine and memory of past posts.
2. **Visualises** — An image generation pipeline (FLUX.1 via Replicate + optional custom LoRA) creates a consistent, photorealistic face for every post.
3. **Posts** — A smart scheduler publishes content autonomously to Twitter/X at randomised, human-like times.
4. **Engages** — Optional services reply to mentions and like relevant content.

The reference persona is **Sienna Fox** — a 23-year-old lifestyle influencer from Los Angeles.

---

## 📍 Current Status (February 2026)

| Component | Technology | Status |
| :--- | :--- | :--- |
| 🐦 Social Platform | Twitter / X | ✅ Production Ready |
| 🎨 Image Generation | FLUX 1 via Replicate | ✅ Production Ready |
| 🧠 LLM Brain | OpenAI GPT-4 / GPT-4o-mini | ✅ Production Ready |
| 💾 Memory | ChromaDB (RAG — avoids repetition) | ✅ Active |
| 🖥️ Control Dashboard | — | 🔴 Planned — Phase 3 |
| 📸 Instagram / Others | — | 🔴 Planned — Phase 4 |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Zirelia Engine                      │
│                                                          │
│  ┌──────────┐   ┌──────────────┐   ┌────────────────┐  │
│  │  Brain   │   │  Imagination  │   │     Hands      │  │
│  │          │   │              │   │                │  │
│  │ LangChain│──▶│ FLUX.1 via   │──▶│ Twitter API    │  │
│  │ LangGraph│   │ Replicate    │   │ (Tweepy)       │  │
│  │ OpenAI   │   │ + LoRA       │   │                │  │
│  │ ChromaDB │   │              │   │                │  │
│  └──────────┘   └──────────────┘   └────────────────┘  │
│                                                          │
│  ┌──────────┐   ┌──────────────┐   ┌────────────────┐  │
│  │Scheduler │   │   Replier    │   │     Liker      │  │
│  │(Celery)  │   │ (Engagement) │   │  (Engagement)  │  │
│  └──────────┘   └──────────────┘   └────────────────┘  │
│                                                          │
│         PostgreSQL · Redis · FastAPI (REST)              │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology |
| :--- | :--- |
| Language | Python 3.10+ |
| AI / Brain | LangChain, LangGraph, OpenAI API |
| Memory | ChromaDB (vector store, RAG) |
| Image Gen | Replicate API (FLUX.1 / SDXL + LoRA) |
| Social API | Tweepy (Twitter/X) |
| Backend | FastAPI, Uvicorn |
| Task Queue | Celery + Redis |
| Database | PostgreSQL 15 |
| Deployment | Docker Compose |

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
- [Git](https://git-scm.com/)
- API keys: **OpenAI**, **Replicate**, **Twitter/X Developer** (Basic access or above)

### 1. Clone

```bash
git clone https://github.com/zirelia/zirelia.git
cd zirelia
```

### 2. Configure

```bash
cp .env.template .env
# Fill in your API keys
nano .env
```

Minimum required variables:

```env
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...
REPLICATE_MODEL_VERSION=black-forest-labs/flux-1.1-pro
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_TOKEN_SECRET=...
TWITTER_BEARER_TOKEN=...
```

### 3. Launch

```bash
docker compose up --build -d
```

This starts: `api` · `scheduler` · `worker` · `db` (PostgreSQL) · `redis`

### 4. Verify

```bash
docker compose ps
docker compose logs scheduler -f
```

### 5. Run a single post manually

```bash
# Dry run (no actual posting)
python main.py --platform twitter --dry-run

# Post now
python main.py --platform twitter --mode hybrid

# Text-only post about a specific topic
python main.py --platform twitter --mode text --topic "morning coffee ritual"
```

---

## ⚙️ CLI Reference

```
python main.py [OPTIONS]

Options:
  --platform  {twitter|instagram|facebook|threads|all}
              Target platform. Default: all (currently maps to twitter)

  --mode      {hybrid|text}
              hybrid = Text + AI-generated image
              text   = Text only

  --topic     TEXT
              Optional topic. Omit for Autonomous Mode
              (bot picks its own topic from persona routine)

  --dry-run   Simulate without posting to social media
```

---

## 🧬 Persona Configuration

The bot's entire personality lives in `config/persona.yaml`. No code changes needed.

```yaml
name: "Sienna Fox"
age: 23
nationality: "American (Los Angeles, CA)"

physical_traits:
  hair: "Light Brown / Dirty Blonde (Wavy)"
  eyes: "Hazel / Warm Brown"
  vibe: "Natural, Sun-kissed"

traits:
  - "Confident"
  - "Playful / Flirty"
  - "Witty"

voice:
  tone: "Seductive but friendly"
  style: "Short, punchy, uses emojis naturally (✨, 😉)"

routine:
  morning:
    - "Waking up in silk sheets"
    - "Morning stretch"
  evening:
    - "Sunset at the beach"
    - "Glass of wine"
```

After editing, restart: `docker compose restart api scheduler`

---

## 🐳 Docker Services

| Service | Description |
| :--- | :--- |
| `api` | FastAPI REST server (port 8000) |
| `scheduler` | Autonomous posting daemon (runs 24/7) |
| `worker` | Celery background task worker |
| `db` | PostgreSQL 15 (persistent storage) |
| `redis` | Message broker / task queue |
| `replier` | Reply to Twitter mentions (manual profile) |
| `liker` | Like relevant content (manual profile) |

Run engagement services manually:

```bash
docker compose --profile manual run replier
docker compose --profile manual run liker
```

---

## 🗺️ Roadmap

| Phase | Goal | Status |
| :--- | :--- | :--- |
| **Phase 1** | Foundation: Twitter, FLUX.1, Smart Scheduler, ChromaDB | ✅ Complete |
| **Phase 2** | Infrastructure: PostgreSQL `pgvector`, Celery integration | 🟡 In Progress |
| **Phase 3** | Control Dashboard (Streamlit/React) | 🔴 Planned |
| **Phase 4** | Multi-Platform: Instagram, LinkedIn, Telegram | 🔴 Planned |
| **Phase 5** | Multimedia: ElevenLabs voice, video clips (Reels/TikTok) | 🔴 Planned |

---

## 📚 Documentation

Full documentation at **[zirelia.github.io/zirelia](https://zirelia.github.io/zirelia/)**

| Guide | Link |
| :--- | :--- |
| Installation | [Getting Started](https://zirelia.github.io/zirelia/getting-started/installation/) |
| Configuration | [Configuration Guide](https://zirelia.github.io/zirelia/getting-started/configuration/) |
| ⚠️ Anti-Ban Strategy | [Account Warm-Up](https://zirelia.github.io/zirelia/guides/account_warmup/) |
| Training a Custom LoRA | [LoRA Training Guide](https://zirelia.github.io/zirelia/guides/lora_training/) |
| Synthetic Dataset | [Dataset Creation](https://zirelia.github.io/zirelia/guides/synthetic_dataset/) |
| Twitter / X Setup | [Twitter Setup](https://zirelia.github.io/zirelia/guides/twitter_setup/) |
| Visual Quality Control | [Visual QC](https://zirelia.github.io/zirelia/guides/visual_quality/) |
| Troubleshooting | [Troubleshooting](https://zirelia.github.io/zirelia/troubleshooting/) |
| API Reference | [API Docs](https://zirelia.github.io/zirelia/reference/scheduler/) |
| Roadmap | [Roadmap](https://zirelia.github.io/zirelia/roadmap/) |

---

## ⚖️ License & Disclaimer

This project is licensed under the **[Elastic License 2.0 (ELv2)](LICENSE)**.
You may use it for personal and internal business use. You may **not** provide it as a managed service to third parties.

> **Use at your own risk.** Automating social media accounts may violate platform Terms of Service. The author takes **no responsibility** for account bans, API costs, or any consequences of using this software. See the [Legal Disclaimer](https://zirelia.github.io/zirelia/legal/) for full terms.

---

## 👤 Author

Built by **[Antonio Trento](https://antoniotrento.net)** — AI Engineer & Developer.

---

<div align="center">
<sub>Made with ❤️ and way too much caffeine.</sub>
</div>
