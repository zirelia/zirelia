# 🗺️ Product Roadmap

This document outlines the development history and future plan for Zirelia.

## 📍 Current State (as of 2026-02-20)

| Component | Technology | Status |
| :--- | :--- | :--- |
| **Social Platform** | Twitter / X | ✅ Production Ready |
| **Image Generation** | FLUX 1 via Replicate (remote) | ✅ Production Ready |
| **LLM Brain** | OpenAI ChatGPT (GPT-4 / GPT-4o-mini) | ✅ Production Ready |
| **Memory** | ChromaDB (local file) | ✅ Active |
| **Instagram / Others** | Not implemented | 🔴 Planned (Phase 4) |
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

## 🟡 Phase 2: Infrastructure Hardening (Next Step)
Currently, we use local files for memory (`chromadb`) and simple loops for scheduling.
*   **PostgreSQL Migration**: Move memory from files to the `db` container using `pgvector`.
*   **Celery Integration**: Move `replier`/`liker` scripts to the `redis` queue for better reliability.
*   **Resource Optimization**: Remove unused containers if we decide to stay lightweight.

## 🟠 Phase 3: Control Center (Dashboard)
Building a UI to manage the bot without using the terminal.
*   **Web Dashboard**: A simple interface (Streamlit or React) to:
    *   View logs live.
    *   Manually approve/reject drafted posts.
    *   Trigger "Force Posting".
    *   Update `persona.yaml` settings visually.

## 🔵 Phase 4: Multi-Platform Expansion
Expanding Sienna's presence beyond Twitter.
*   **Instagram**:
    *   Post images to Feed.
    *   Post Stories using the `mobile-vertical` aspect ratio.
*   **LinkedIn**:
    *   Professional-tone posts (using a different System Prompt).
*   **Telegram/Discord**:
    *   Chatbot mode for direct interaction with fans.

## 🟣 Phase 5: Multimedia Evolution
*   **Voice**: Use ElevenLabs to give Sienna a voice for audio messages.
*   **Video**: Use Remotion or Luma Dream Machine to generate short video clips (Reels/TikToks).
*   **Real-Time Reactivity**: Ability to "see" images in replies (Vision API) and comment on them.
