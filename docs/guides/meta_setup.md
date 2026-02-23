# Meta Developer Setup (Instagram & Threads)

This guide provides a step-by-step walkthrough on how to set up the necessary Developer Accounts, Apps, and API Tokens to allow Zirelia to post autonomously to **Instagram** and **Threads**.

> [!IMPORTANT]
> **Prerequisites before starting:**
> 1. A standard **Facebook account** (used to log into the Developer Portal).
> 2. An **Instagram Professional Account** (Creator or Business). Both are **100% free** to switch to.
> 3. A **Threads account** linked to the same Instagram profile.
> 4. A **Facebook Page** linked to the Instagram account (required by the Meta API for Instagram access).
> 
> 💡 **Cost Note**: The Instagram and Threads APIs, as well as Developer Accounts, are **completely free** to use. Meta does not charge for API requests like Twitter does.

---

## Part 0: Account Creation Strategy (Anti-Ban)

Meta's security algorithms are extremely aggressive against newly created accounts that immediately try to use APIs. **DO NOT create a "fake" Facebook profile for your AI.** You will be banned within 24 hours.

Follow this exact sequence to establish trust:

1. **The Email**: Use the **same email address** (e.g., Gmail) that you used for your AI's Twitter/X account. Consistency builds trust cross-platform.
2. **Instagram & Threads**:
   * Create the Instagram account **from a smartphone app** (not a desktop browser).
   * Install the Threads app and log in using the newly created Instagram credentials.
   * In the Instagram app settings, switch the account to a **Professional Account** (Creator or Business).
3. **The Facebook Connection (CRITICAL)**:
   * Log into your **REAL, personal Facebook account** (the one you use every day).
   * Create a new **Facebook Page** for your AI (e.g., "Sienna Fox"). You don't need to post anything here; it acts as a legal/technical bridge.
   * In the settings of this new Facebook Page, go to "Linked Accounts" and **connect the AI's Instagram account**.
   * Because your real personal account has a high "Trust Score", Meta allows the Page (and its linked Instagram) to use APIs safely.

---

## Part 1: Setting up the Meta App

1. Go to the [Meta for Developers Portal](https://developers.facebook.com/) and log in with your Facebook account.
2. If this is your first time, register as a Meta Developer.
3. Click on **My Apps** in the top right corner, then click **Create App**.
4. Select **Other** for the use case and click Next.
5. Select **Business** as the app type and click Next.
6. Give your app a name (e.g., "Zirelia AutoPoster") and enter an App Contact Email. Leave the Business Account unassigned for now, unless you have one prepared. Click **Create App**.

---

## Part 2: Configuring Instagram Graph API

The Instagram Graph API allows you to publish photos and Videos (Reels) to an Instagram Professional account.

1. On your App Dashboard, scroll down to **Add products to your app**.
2. Find **Instagram Graph API** and click **Set Up**.
3. In the left sidebar, under **Instagram Graph API**, click on **API Setup**.
4. You will see a button to **Add Facebook Login for Business**. Click it, as this is the underlying authentication mechanism Meta uses.
5. Follow the prompts to add the product.
6. Now, you need to generate an **Access Token**. The easiest way to do this without writing custom OAuth code is using the **Graph API Explorer**:
    * Go to **Tools > Graph API Explorer** from the top menu.
    * In the "Meta App" dropdown, select your newly created app.
    * Under "User or Page", select **Get Page Access Token**. You will be prompted to log in and authorize the app to access your Facebook Page and linked Instagram Account.
    * Make sure to grant the following permissions when prompted: 
        * `instagram_basic`
        * `instagram_content_publish`
        * `pages_show_list`
        * `pages_read_engagement`
    * Once authorized, you will see a token in the "Access Token" field. **This token is temporary (usually valid for 1 hour).**

### Getting a Long-Lived Access Token for Instagram

You need a token that doesn't expire every hour for an autonomous bot.

1. Still in the Graph API Explorer, click the small blue exclamation mark (ℹ️) next to your short-lived token.
2. Click **Open in Access Token Tool**.
3. At the bottom of the tool page, click **Extend Access Token**.
4. This will generate a long-lived token (usually valid for 60 days). **Copy this token**. This will be your `META_ACCESS_TOKEN` in the `.env` file.

### Finding your IDs

You also need your Facebook Page ID and Instagram Account ID for the API calls.

1. In the Graph API Explorer, enter `me/accounts` in the query box and click **Submit**.
2. Find the ID of the Facebook Page linked to your Instagram account in the JSON response. This is your `FACEBOOK_PAGE_ID`.
3. Now, enter `{FACEBOOK_PAGE_ID}?fields=instagram_business_account` in the query box (replace with your actual ID) and click **Submit**.
4. The JSON response will contain your `instagram_business_account` ID. This is your `INSTAGRAM_ACCOUNT_ID`.

---

## Part 3: Configuring Threads API

The Threads API is separate from the Instagram Graph API but is managed within the same Meta App.

1. Go back to your App Dashboard.
2. Click **Add Product** in the left sidebar.
3. Find **Threads API** and click **Set Up**.
4. In the left sidebar under Threads API, go to **Settings**.
5. You need to configure the OAuth settings. Add `https://localhost` or your local development URL to the **Valid OAuth Redirect URIs**.
6. Just like with Instagram, you need an Access Token. Meta provides a [Threads API Token Generator Tool](https://developers.facebook.com/docs/threads/get-started) in their documentation specifically for testing.
    * Alternatively, you can use the Graph API Explorer again, but select the Threads App permissions (`threads_basic`, `threads_content_publish`).
7. Generate a long-lived token following a similar process to Instagram (exchanging the short-lived token for a long-lived one via the `/oauth/access_token` endpoint). 
    * *Note: Threads tokens also typically expire after 60 days and need refreshing.*

---

## Part 4: Updating `.env` and `mkdocs.yml`

Now that you have your credentials, you will add them to the `.env` file (these variables are already defined in `docker-compose.yml`).

```env
# Meta / Instagram Settings
META_APP_ID=your_app_id_from_dashboard
META_APP_SECRET=your_app_secret_from_dashboard
META_ACCESS_TOKEN=your_long_lived_page_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id

# Threads Settings (Often uses the same App ID but different tokens depending on setup)
THREADS_ACCESS_TOKEN=your_long_lived_threads_token
THREADS_USER_ID=your_threads_user_id
```

### Important Notes for Production

*   **Token Expiration**: Meta's long-lived tokens typically expire after 60 days. In Phase 4 development, we will need to implement an automated Token Refresh script to keep the bot running indefinitely without manual intervention.
*   **App Review**: While you are the only user of the app (Admin role), you do **not** need to submit your app for Meta App Review. You can remain in "Development" mode. However, if the tokens expire frequently, switching to "Live" mode might be necessary, though this requires fulfilling Meta's business verification requirements.
