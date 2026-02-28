# 🗺️ Product Roadmap

This document outlines the development history and future plan for Zirelia.

## 📍 Current State (as of 2026-02-28)

| Component | Technology | Status |
| :--- | :--- | :--- |
| **Twitter / X** | Tweepy (OAuth 1.0a) | ✅ Production Ready |
| **Instagram** | Meta Graph API v18.0 | ✅ Production Ready |
| **Facebook** | Meta Graph API v18.0 | ✅ Production Ready |
| **Threads** | Threads API v1.0 | ✅ Production Ready |
| **Image Generation** | FLUX 1 via Replicate (remote) | ✅ Production Ready |
| **LLM Brain** | OpenAI ChatGPT (GPT-4 / GPT-4o-mini) | ✅ Production Ready |
| **Memory** | ChromaDB (local file) | ✅ Active |
| **Threads Token Renewal** | Auto-refresh at 50 days | ✅ Active |
| **Content Safety** | LLM-level + topic filtering | ✅ Active |
| **Local Image Gen** | Not implemented | 🔴 Planned |
| **Control Dashboard** | Not implemented | 🔴 Planned (Phase 3) |

---

## 🟢 Phase 1: Foundation (Completed) ✅
*   **Persona Engine**: Use LLM (OpenAI) to generate thoughts and personality.
*   **Visual Identity**: LoRA model (Replicate) for consistent face generation.
*   **Smart Scheduler**: Timezone-aware posting (Los Angeles) with holiday awareness.
*   **Twitter Integration**: Automated posting and basic "Safe Mode" engagement.
*   **Documentation**: MkDocs site for setup and guides.

---

## 🟢 Phase 2: Multi-Platform Expansion (Completed) ✅
*   **Facebook**: Automated Page posting via Graph API with permanent token.
*   **Instagram**: Automated posting with 3-step container flow (create → poll → publish).
*   **Threads**: Separate API integration with viral engagement strategy.
*   **Threads Token Auto-Renewal**: Automatic 60-day token refresh (at 50 days).
*   **Content Safety**: LLM-enforced moderation (no lingerie/underwear on any platform).
*   **Threads Viral Strategy**: Hot takes, this-or-that questions, relatable rants, IG cross-promo.

---

## 🟡 Phase 3: Infrastructure Hardening (Next Step)
*   **PostgreSQL Migration**: Move memory from files to the `db` container using `pgvector`.
*   **Celery Integration**: Move `replier`/`liker` scripts to the `redis` queue for better reliability.
*   **Resource Optimization**: Remove unused containers if we decide to stay lightweight.

## 🟠 Phase 4: Control Center (Dashboard)
Building a UI to manage the bot without using the terminal.
*   **Web Dashboard**: A simple interface (Streamlit or React) to:
    *   View logs live.
    *   Manually approve/reject drafted posts.
    *   Trigger "Force Posting".
    *   Update `persona.yaml` settings visually.

## 🔵 Phase 5: Multimedia Evolution
*   **Voice**: Use ElevenLabs to give Sienna a voice for audio messages.
*   **Video**: Use Remotion or Luma Dream Machine to generate short video clips (Reels/TikToks).
*   **Real-Time Reactivity**: Ability to "see" images in replies (Vision API) and comment on them.
