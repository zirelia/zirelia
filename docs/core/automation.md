# Automation (Smart Scheduler)

Zirelia does not rely on static cron jobs, but uses a Python-based **Smart Scheduler** to ensure posts feel organic and human-like.

## How it Works
The scheduler runs in an infinite loop inside the `scheduler` Docker container.

### 1. Daily Schedule Generation
Every day at midnight (or upon restart), the scheduler:
*   Checks the date for **Special Events/Holidays** (e.g., Valentine's Day).
*   Randomly selects a minute within predefined "windows":
    *   **Morning**: 08:00 - 10:00
    *   **Afternoon**: 13:00 - 15:00
    *   **Evening**: 19:00 - 22:00

### 2. Execution loop
*   Sleeps until the next scheduled time.
*   Wakes up and executes `main.py` via subprocess (ensuring a fresh memory state for each run).
*   Logs all activity to the Docker logs.

## Holiday Awareness
The scheduler is aware of major holidays and will prioritize themed content on those dates.
This logic is defined in `core/automation/scheduler.py`.

## Key Files
*   `core/automation/scheduler.py`: Logic for scheduling and holiday checks.
*   `run_scheduler.py`: The entry point script for the Docker container.
