# Welcome to Zirelia Docs 🧜‍♀️

**Zirelia** is an advanced, autonomous Virtual Influencer Engine capable of generating its own personality, visual identity, and social media content.

It combines **LLMs (OpenAI/Anthropic)** for the "Brain", **Image Diffusion Models (FLUX.1/SDXL)** for the "Imagination", and **Social APIs** for the "Hands", all wrapped in a Dockerized architecture that runs 24/7 on edge devices like a Raspberry Pi.

## 📍 Current Tech Stack (as of 2026-02-28)

| Component | Technology | Status |
| :--- | :--- | :--- |
| 🐦 Twitter / X | Tweepy (OAuth 1.0a) | ✅ Production Ready |
| 📸 Instagram | Meta Graph API v18.0 | ✅ Production Ready |
| 📘 Facebook | Meta Graph API v18.0 | ✅ Production Ready |
| 🧵 Threads | Threads API v1.0 (Viral Strategy) | ✅ Production Ready |
| 🎨 Image Generation | FLUX 1 via Replicate (remote API) | ✅ Production Ready |
| 🧠 LLM Brain | OpenAI ChatGPT (GPT-4 / GPT-4o-mini) | ✅ Production Ready |
| 🔑 Token Management | Auto-renewal for Threads (60-day tokens) | ✅ Active |
| 🛡️ Content Safety | LLM-enforced outfit moderation | ✅ Active |
| 🖥️ Control Dashboard | Not implemented | 🔴 Planned |

> [!CAUTION]
> **New account? Read the Warm-Up guide first!**
> Starting the bot on a new account without any credibility baseline is the #1 cause of permanent shadowbans. Read the full guide before doing anything else.
> **→ [Account Warm-Up & Anti-Ban Guide](guides/account_warmup.md)**

## 🚀 Key Features

*   **🧠 Persona Engine**: A LangChain-based brain that maintains a consistent personality, memories, and writing style defined in a simple YAML config.
*   **🎨 Hyper-Realistic Visuals**: Integrates with Replicate to generate consistent character images using custom LoRA models (e.g., *Sienna Fox*).
*   **🤳 Multi-Platform Posting**: Autonomous posting to Twitter, Instagram, Facebook, and Threads — each with platform-optimized content.
*   **🧵 Threads Viral Strategy**: Hot takes, this-or-that questions, relatable rants, and subtle Instagram cross-promotion.
*   **🔑 Auto Token Renewal**: Threads tokens are automatically refreshed 10 days before their 60-day expiration.
*   **🛡️ Content Safety**: AI-enforced outfit moderation and visual quality control before posting.
*   **🤳 Smart Scheduler**: Randomized posting times (Morning, Afternoon, Evening) with holiday awareness.
*   **🔌 Easy Deployment**: Fully Dockerized stack (API, Worker, Scheduler, Redis, Postgres) ready for `docker compose up`.

## 📚 Documentation Structure

*   [**⚠️ Account Warm-Up & Anti-Ban**](guides/account_warmup.md): **Read this first.** How to onboard a new account safely.
*   [**Getting Started**](getting-started/installation.md): Set up the engine on your local machine or server.
*   [**Core Architecture**](core/brain.md): Understand how the Brain, Imagination, and Hands work together.
*   [**Guides**](guides/lora_training.md): Learn how to train your own LoRA face model and create synthetic datasets.
*   [**API Reference**](reference/scheduler.md): Technical details for developers.
*   [**Roadmap**](roadmap.md): What's next.
*   [**⚖️ Legal Disclaimer**](legal.md): Terms of use, liability limits, and compliance notes.

---

> [!WARNING]
> Zirelia is provided "as-is" for educational purposes. The developers take **no responsibility** for account bans, API costs, or any consequences of using this software. See [Legal Disclaimer](legal.md).

*Built with ❤️ by Antonio Trento.*
