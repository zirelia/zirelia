# Engagement Automation Guide (Experimental) 🧪

This guide explains how to use the **Auto-Replier** and **Auto-Liker** modules.
These are **Risk-Heavy Features**. Use with extreme caution.

## 🛑 Warning

!!! danger "Risk of Suspension"
    Automated liking and replying is the #1 reason for Twitter bans.
    We have implemented "Safe Mode" limits, but **you use this at your own risk**.

## 1. Setup

These services are **STOPPED** by default. They will not start with `docker compose up`.
You must launch them manually.

### Profile: `manual`
We use a Docker Profile called `manual` to hide them from the main stack.

## 2. The Replier (Auto-Reply to Mentions) 💬
This bot checks your notifications every 30 minutes.

*   **What it does**: Replies to people who @mention you.
*   **Safety Limit**: Max 5 replies per run.
*   **To ID**: It keeps a history in `engagement_replied.json` to avoid double-replying.

**To Start:**
```bash
docker compose --profile manual up -d replier
```

**To Stop:**
```bash
docker compose stop replier
```

**To Check Logs:**
```bash
docker compose logs -f replier
```

## 3. The Liker (Auto-Like Keywords) ❤️
This bot searches for tweets (e.g., #DigitalArt) every 60 minutes.

*   **What it does**: Likes relevant tweets to grow visibility.
*   **Safety Limit**: Max 1 like per run.
*   **Filter**: Skips Retweets, Replies, and own tweets.

**To Start:**
```bash
docker compose --profile manual up -d liker
```

**To Stop:**
```bash
docker compose stop liker
```

## 4. Configuration
You can tweak the python files directly if you want to change keywords or limits:
*   `core/engagement/replier.py`: Change `MAX_REPLIES_PER_RUN` or `CHECK_INTERVAL_SECONDS`.
*   `core/engagement/liker.py`: Change `SEARCH_QUERIES` list.

_Remember to rebuild after code changes:_
```bash
docker compose build
```
