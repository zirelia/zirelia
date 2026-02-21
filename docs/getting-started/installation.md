# Installation Guide

Zirelia is designed to run in **Docker containers**, making it easy to deploy on any system, including Edge devices like **Raspberry Pi (ARM64)** or standard cloud servers (Linux/Windows).

## Prerequisites

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) or Docker Engine
*   [Git](https://git-scm.com/)
*   API Keys:
    *   **OpenAI** (for the Brain / Content Text)
    *   **Replicate** (for the Imagination / Image Gen)
    *   **Twitter/X** (for Posting)

---

## 🐳 Option 1: Docker (Recommended)

This is the production-ready method. It handles the database, Redis, API, and Scheduler automatically.

### 1. Clone the Repository
```bash
git clone https://github.com/antoniotrento/Zirelia.git
cd Zirelia
```

### 2. Configure Environment
Copy the example environment file and fill in your keys.
```bash
cp virtual_influencer_engine/.env.example virtual_influencer_engine/.env
# Edit the file with your API keys
nano virtual_influencer_engine/.env
```
*(See [Configuration](configuration.md) for details on each variable)*

### 3. Build & Run
Launch the entire stack (API, DB, Scheduler, Worker):
```bash
docker compose up --build -d
```

### 4. Verify Status
Check if all services are running:
```bash
docker compose ps
```
You should see:
*   `api`: The HTTP Server (FastAPI)
*   `scheduler`: The Automation Daemon
*   `worker`: The Background Task Worker (Celery)
*   `db`: PostgreSQL
*   `redis`: Queue Broker

---

## 💻 Option 2: Local Python Setup

Use this for development or debugging logic without container overhead.

### 1. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r virtual_influencer_engine/requirements.txt
```

### 3. Run Manually
To generate a single post manually:
```bash
python virtual_influencer_engine/main.py --platform twitter
```

To run the scheduler locally:
```bash
python virtual_influencer_engine/run_scheduler.py
```

---

> [!WARNING]
> **Disclaimer**: By installing and running Zirelia, you accept full responsibility for its use. The developers take no liability for API costs, account bans, or any other consequences. This software is provided "as-is". See the [Legal Disclaimer](../legal.md) for the full terms.
