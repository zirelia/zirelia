# Setting up Twitter (X) Integration

To enable your Virtual Influencer to post autonomously, you need access to the Twitter API.

!!! warning "STOP: Read This Before Creating an Account!"
    If you create a **new Twitter account** and immediately connect it to an API/Bot, **Twitter WILL Shadowban you** (hide your profile from search).

    **To avoid this:**
    1.  Create the account on a phone.
    2.  Add a profile pic, bio, and banner.
    3.  **Use it manually for 48-72 hours**: Like, Retweet, Follow, and Reply to real people.
    4.  Only THEN generate API keys.
    
    See [Troubleshooting](../troubleshooting.md) for more details.

## 1. Create a Developer Account
1.  Go to the [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard).
2.  Sign up for the **Free Plan** (allows ~1,500 posts/month).
3.  Create a Project and an App.

## 2. Generate Keys & Tokens
You need 4 specific credentials.

### API Key & Secret
Location: `Keys and Tokens` -> `Consumer Keys`.
*   **API Key**: Copy to `TWITTER_API_KEY`.
*   **API Key Secret**: Copy to `TWITTER_API_SECRET`.

### Access Token & Secret (Critical Step)
By default, access tokens are "Read Only". You must change this BEFORE generating them.

1.  Go to **User authentication settings** -> **Edit**.
2.  App permissions: select **Read and Write**.
3.  Type of App: **Automated App or Bot**.
4.  Redirect URL: `http://localhost:8000/callback` (Required placeholder).
5.  Website URL: `https://example.com` (Required placeholder).
6.  Save.

**NOW** go back to `Keys and Tokens` -> `Authentication Tokens`.
Generate (or Regenerate) your **Access Token and Secret**.

*   **Access Token**: Copy to `TWITTER_ACCESS_TOKEN`.
*   **Access Token Secret**: Copy to `TWITTER_ACCESS_TOKEN_SECRET`.

## 3. Configure `.env`
Add these keys to your `.env` file as shown in the [Configuration Guide](../getting-started/configuration.md).

---

> [!WARNING]
> **Disclaimer**: Automating a Twitter/X account may violate Twitter's [Terms of Service](https://twitter.com/en/tos) and [Automation Rules](https://help.twitter.com/en/rules-and-policies/twitter-automation). The developers of Zirelia take **no responsibility** for account bans, suspensions, or any consequences arising from your use of this software. Use at your own risk. See [Legal Disclaimer](../legal.md).
