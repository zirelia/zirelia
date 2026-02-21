# Account Warm-Up & Silent Ban Prevention 🔥

> [!CAUTION]
> **Read this guide BEFORE starting the bot.** Skipping this phase is the #1 cause of shadowbans on new accounts.

## The Problem: Zero Credibility

Twitter/X uses sophisticated anti-spam algorithms. A **new account that posts automatically and regularly** is immediately flagged as a bot. The result is a **Shadowban**: your posts exist, but they are invisible to anyone not already following the account. A visitor browsing in incognito will see nothing.

> [!NOTE]
> A Shadowban is not a permanent punishment. It's a temporary quarantine that can be resolved by building organic credibility.

---

## Phase 1: Pre-Launch (Week 1-2) ✋

**Do NOT start the bot.** This is a manual credibility-building period.

### Human Checklist
- [ ] Complete the profile 100% (Bio, link, profile picture, cover photo).
- [ ] Add a phone number for verification (significantly reduces flags).
- [ ] Manually **like at least 50 posts** in your niche.
- [ ] **Follow 20-30 relevant accounts**.
- [ ] Write **3-5 manual tweets** to "break the ice". You can use `--dry-run` for inspiration, but post them manually.
- [ ] Reply to a few comments on other people's posts.

### Goal
Make the algorithm believe there is a real human using the account normally.

---

## Phase 2: Soft Launch (Week 3-4) 🐢

You can now start the bot, but with the brakes on.

### Recommended Configuration

In the `.env` file on your Raspberry Pi:

```env
# PHASE 2: Gradual post-launch
MAX_DAILY_POSTS=1
```

Then restart the scheduler:
```bash
docker compose restart scheduler
```

### The Golden Rule
**One post per day, during peak hours** (morning or evening). Nothing more.

> [!WARNING]
> Twitter's algorithm values **consistency** more than frequency. One post per day for 30 days is worth 100x more than 30 posts in a single day.

---

## Phase 3: Growth (Month 2+) 🚀

After 4 weeks with no bans and positive engagement, you can gradually increase frequency.

| Phase | Posts/Day | Notes |
| :--- | :--- | :--- |
| **Pre-Launch (Week 1-2)** | 0 (human only) | Build credibility |
| **Soft Launch (Week 3-4)** | 1 | `MAX_DAILY_POSTS=1` |
| **Growth (Month 2)** | 2 | `MAX_DAILY_POSTS=2` |
| **Cruise (Month 3+)** | 3 | `MAX_DAILY_POSTS=3` |

### Changing the Frequency
Edit the `.env` file:
```env
MAX_DAILY_POSTS=2
```
Then restart:
```bash
docker compose restart scheduler
```

---

## Diagnosis: Am I Shadowbanned?

Open Twitter/X in a **private/incognito window** and search for your username `@YourHandle`.

| Symptom | Diagnosis |
| :--- | :--- |
| Posts **don't appear** even when searching the username | ⛔ Shadowban Confirmed |
| Posts **appear** on the profile but not in hashtag searches | ⚠️ Partial Ban (Search Ban) |
| Posts appear everywhere | ✅ All good |

---

## Cure: I'm Shadowbanned, What Do I Do?

1.  **Stop the bot immediately:**
    ```bash
    docker compose stop scheduler
    ```
2.  **Wait 3-7 days** without posting anything.
3.  **Manual human activity**: Log into the account, like a few posts, reply to some comments.
4.  **Restart with Phase 2** (`MAX_DAILY_POSTS=1`).

> [!TIP]
> Temporary shadowbans usually resolve within 3-5 days if the account does nothing suspicious in the meantime.

---

## ⚖️ Disclaimer

The developers of Zirelia **take no responsibility** for account suspensions, shadowbans, or any other penalties imposed by Twitter/X or any other platform. Following this guide reduces risk but **cannot guarantee** immunity from platform enforcement actions. Use this software at your own risk and always comply with the platform's current [Terms of Service](https://twitter.com/en/tos). See the [full Legal Disclaimer](../legal.md) for details.
