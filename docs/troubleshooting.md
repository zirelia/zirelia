# Troubleshooting & common Issues

This guide addresses common problems you might encounter when deploying your Virtual Influencer.

## 👻 Twitter Account Visibility ("Ghost Account" / Shadowban)

### The Problem
You created a new Twitter account, paid for API access, and started posting.
*   **You** can see your posts when logged in.
*   **Others** (logged out or other users) see "This account does not exist" or cannot find your profile in search.
*   Your posts get 0 impressions.

### Why is this happening?
This is **Twitter's Anti-Spam Protection** for new accounts, especially those using the API immediately.
If a brand new account (< 48 hours old) starts posting via API without "human" behavior first, Twitter flags it as a potential bot farm and hides it from public view (Search Ban / Ghost Ban).

### How to Fix
You are likely **NOT blocked**, just **hidden**.

1.  **Stop the Bot immediately**: Do not let the API post for 24-48 hours.
2.  **Warm Up Manually**:
    *   Log in to the account on a phone (official app).
    *   Change your profile picture and bio if you haven't.
    *   Follow 5-10 verifies accounts (Blue checks).
    *   Like and Retweet a few real posts *manually*.
    *   Reply to a post with text (e.g., "Agree!" or "Nice").
3.  **Wait**: New accounts often take 24-72 hours to be indexed by search.
4.  **Appeal**: If it persists after 3 days of manual usage, contact Twitter Support via the Help Center.

---

## 🛑 "403 Forbidden" or "401 Unauthorized" on Twitter

### Cause
*   **401**: Your API Keys or Access Tokens are wrong. Did you regenerate them *after* changing permissions to Read/Write?
*   **403**: Your App lacks "Write" permissions.

### Solution
1.  Go to [Twitter Developer Portal](https://developer.twitter.com).
2.  Check **User Authentication Settings**.
3.  Ensure **App Permissions** is set to **Read and Write**.
4.  **Regenerate** the *Access Token and Secret* (Consumer Keys stay the same).
5.  Update your `.env` file.

---

## 🖼️ Replicate Error: "NSFW Content Detected"

### The Problem
The image generator returns an error instead of an image URL.

### Cause
The safety filter on Replicate (or the model itself) flagged your prompt.
"Seductive", "Hot", or "Lingerie" keywords can trigger this depending on the model's strictness.

### Solution
*   **Tone down the prompt**: In `core/image_gen/pipeline.py`, ensure the injected keywords aren't too explicit.
*   **Use a different model**: Uncensored models exist but may be lower quality. We stick to FLUX because it's SOTA (State of the Art) and usually compliant with ToS.

---

## 📋 Monitor & Logs

To see what the bot is doing, use `docker compose logs`.

### 1. Watch the Scheduler (The Brain)
To see when the next post is scheduled:
```bash
docker compose logs -f scheduler
```
*   Look for lines like: `📅 SCHEDULE FOR 2026-02-18:...`

### 2. Watch the API (The Hands)
To see errors during the actual posting process:
```bash
docker compose logs -f api
```

### 3. Check All Services
To make sure everything is running (and not "Exited"):
```bash
docker compose ps
```
