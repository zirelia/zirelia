# Setup Guide

## Requirements
- Python 3.10+
- Docker & Docker Compose (optional but recommended)
- PostgreSQL (or SQLite for local testing)
- Redis (for Celery)
- OpenAI API Key (or other LLM provider)
- HuggingFace Token (for SDXL)

## Installation

### 1. Local Development (Python Virtual Environment)
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/virtual-influencer-engine.git
   cd virtual-influencer-engine
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```bash
   touch .env
   ```
   Add the following variables:
   ```env
   DATABASE_URL=sqlite:///./influencer.db
   REDIS_URL=redis://localhost:6379/0
   OPENAI_API_KEY=your_openai_key
   HF_TOKEN=your_huggingface_token
   TWITTER_API_KEY=your_key
   # Add other platform keys as needed
   ```

5. **Run the demo**:
   ```bash
   python demo.py
   ```

### 2. Docker Deployment
1. **Ensure Docker is running**.
2. **Build and run**:
   ```bash
   docker compose up --build
   ```
   This will start the API, Database, Redis, and Worker services.

## Configuration
- Modify `config/persona.yaml` to change the influencer's personality.
- Modify `config/settings.yaml` for system-wide settings.
