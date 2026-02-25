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

---

## 🔑 Meta Graph API: "User Token" Revert Bug & Empty `me/accounts`

### The Problem
When trying to obtain a **Page Access Token** via the Graph API Explorer:
1. The "User or Page" dropdown **reverts back to User Token** immediately after you select your Page.
2. Querying `me/accounts` returns an empty array `{"data": []}` instead of your page details.

### Why is this happening?
Meta often loses the connection between your developer App and your Page's permissions, or it hides the page selection screen during login for new apps.

### Solutions (Try in order)

#### Solution 1: "Edit previous access" Trick (Most Common)
Meta has recently started hiding the page selection checkboxes during the login popup.
1. In a normal browser tab, go to **Facebook > Settings & privacy > Settings > Business Integrations** and **Remove** your App.
2. In the Graph API Explorer, verify you are requesting a User Token, then click **Generate Access Token**.
3. When the Facebook popup appears, **DO NOT click "Continue as [Your Name]" immediately**.
4. Click on **"Edit settings"**, **"Choose what you allow"**, or **"Edit previous access"**.
5. Manually check the boxes next to your Facebook Page and Instagram Account.
6. Confirm and close the popup. Now try selecting your Page from the dropdown again.

#### Solution 2: Add Business Permissions
If your page is linked to a Meta Business Suite, Meta secretly blocks token generation unless you request business access.
1. In the Graph API Explorer permissions box, add `business_management`.
2. Add `pages_manage_metadata`.
3. Click **Generate Access Token** again (make sure to select the page in the popup).
4. Try selecting your Page token.

#### Solution 3: Align Business Manager (Development Mode)
If your App is in "Development" mode, Meta prevents token generation if the App and the Page are not in the exact same Meta Business Manager / Portfolio.
1. Go to your App dashboard on the Meta Developer Portal.
2. Navigate to **Settings -> Basic**.
3. Scroll down to **Business Portfolio**.
4. Select the specific Business Manager that owns the Facebook Page. If it says "No Business Manager selected", you must select the correct one and save.
5. Return to the Graph API Explorer and try again.
