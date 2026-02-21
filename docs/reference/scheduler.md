# SmartScheduler Reference

Path: `virtual_influencer_engine/core/automation/scheduler.py`

## Class: `SmartScheduler`

The autonomous engine that determines when to post.

### Methods

#### `__init__(self)`
Initializes the scheduler.

#### `generate_daily_schedule(self)`
Calculates the posting times for the current day.
*   **Logic**:
    *   Checks if today is a holiday (defined in `HOLIDAYS` dictionary).
    *   Generates 3 slots: Morning (08-10), Afternoon (13-15), Evening (19-22).
    *   Randomizes the minute for each slot.
*   **Returns**: Nothing (updates `self.schedule`).

#### `run_loop(self)`
Starts the infinite loop.
*   Checks if date has changed (to regenerate schedule).
*   Finds next pending post.
*   Sleeps until execution time.
*   Calls `_execute_post`.

#### `_execute_post(self, post)`
Internal method to trigger `main.py` via subprocess.
*   **Args**: `post` (dict containing time, label, topic).
*   **Command**: `python virtual_influencer_engine/main.py --platform twitter --topic [TOPIC]`
