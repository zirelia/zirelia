# AI Virtual Influencer Engine

## Overview
A comprehensive, modular, and automated system to create, manage, and grow a virtual influencer persona across Twitter/X, Threads, Instagram, and Facebook.

## Features
- **Persona Engine**: LLM-driven personality with persistent memory.
- **Image Generation**: Consistent identity using Stable Diffusion XL + LoRA + ControlNet.
- **Content Engine**: Platform-optimized captions and hashtags.
- **Social Automation**: Automated posting, scheduling, and engagement.
- **Safety Engine**: Advanced anti-ban, rate-limiting, and human-behavior emulation.
- **Growth Engine**: Analytics-driven optimization loop.
- **Dashboard**: Web-based control panel (API backend provided).

## Documentation
- [Installation & Setup](docs/SETUP.md)
- [Safety & Anti-Ban Strategy](docs/SAFETY_STRATEGY.md)

## Architecture
- **Backend**: Python, FastAPI
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **AI**: PyTorch, Diffusers, OpenAI/Claude API

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `config/settings.yaml` and `config/persona.yaml`.
4. Run the demo script: `python demo.py`
5. Run with Docker: `docker compose up --build`

## Configuration
- `settings.yaml`: API keys, database URLs, platform credentials.
- `persona.yaml`: Influencer personality traits, tone, and backstory.
