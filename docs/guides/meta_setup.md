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

## Part 1: Setting up the Meta App (Business Method)

> [!CAUTION]
> **IMPORTANT: Ignore Business Verification**
> On your dashboard, you might see a warning asking you to "Verify your Business" or telling you the app is "Unverified." **IGNORE THIS COMPLETELY.** Do not upload any documents. Since you are building an app solely for your own use, the app can remain in "Development" or "Unverified" status forever.

Meta frequently changes its interface, often hiding options for independent developers. To get access to Instagram without blocks, follow **exactly** these steps to force the creation of a "Business" app:

1. Go to the [Meta for Developers Portal](https://developers.facebook.com/) and log in with your personal Facebook account.
2. Click on **My Apps** in the top right corner, then click the green **Create App** button.
3. On the *"What do you want your app to do?"* screen, **IGNORE all the main options**. Scroll to the very bottom of the page, select **Other** and click Next.
4. On the *"Select an app type"* screen, choose **Business** and click Next.
5. Give your app a name (e.g., "Zirelia AutoPoster"). Leave the Business Account as **No Business Account selected**. Click **Create App**.

---

## Part 2: Adding Products (Instagram and Login)

Once the Business App is created, you will land on a Dashboard with large panels called "Products". You must add two specific products to make everything work without errors:

1. Scroll down the "Add products to your app" page.
2. Find the **Instagram** (or *Instagram Graph API*) panel and click **Set Up**. The left menu will update, ignore it and return to the Dashboard (or click *Add Product*).
3. Find the **Facebook Login for Business** panel and click **Set Up**. *(This step is CRITICAL to allow the login window to open later, preventing the "Feature Unavailable" error).*

### 2.1 Enter the Mandatory Privacy Link
Meta blocks the login window if a dummy Privacy URL is missing:
1. From the left menu of your App, go to **Settings > Basic**.
2. Find the **Privacy Policy URL** field. Enter any link (e.g., `https://google.com` or your GitHub). Scroll down and click **Save changes**.

---

## Part 3: Generating the Token (Graph API Explorer)

Forget the chaotic app dashboard and go straight to the official developer tool. This is the only safe way to avoid getting stuck:

1. Open this direct link: 👉 **[Graph API Explorer](https://developers.facebook.com/tools/explorer/)**
2. In the right menu "Meta App", select your app (if not already selected).
3. Under **"User or Page"**, click the dropdown and choose **Get User Access Token**.
4. A Facebook popup will open: log in with your personal account and **select all your Pages and Instagram accounts**. Confirm. (If you previously got a "Feature Unavailable" error here, the Privacy URL and Facebook Login fix from Part 2 solved it).
5. Under the **Permissions** section (still on the right), use the search bar or dropdowns to **add these 5 items**:
    * `instagram_basic`
    * `instagram_content_publish`
    * `pages_show_list`
    * `pages_read_engagement`
    * `pages_manage_posts` (Strictly required to publish on the Facebook Page)
    *(If you want Threads, also add `threads_basic` and `threads_content_publish`).*
6. Click the giant green button **Generate Access Token** and re-confirm the Facebook popup.
7. WE ARE CLOSE: Return to the **User or Page** dropdown and open it. Click on the **Name of your Page** (e.g., "Sienna Fox").
8. The long string in the center of the screen will change: **that is your Page Token**! Copy it somewhere safe.

### Making the Token Long-Lived

You need a token that doesn't expire every hour for an autonomous bot.

1. Still in the Graph API Explorer, click the small blue exclamation mark (ℹ️) next to your short-lived token.
2. Click **Open in Access Token Tool**.
3. At the bottom of the tool page, click **Extend Access Token**.
4. This will generate a long-lived token (usually valid for 60 days). **Copy this token**. This will be your `META_ACCESS_TOKEN` in the `.env` file.

### Finding your IDs (Facebook Page ID and Instagram Account ID)

To make the posting script work (and paste them into your `.env` file), Zirelia needs to know exactly the ID of the bridge Page and the ID of the Instagram profile. The Graph API Explorer offers the simplest way without struggling with JSON parsing:

1. Go back to the **Graph API Explorer** (ensure your Page Token is still loaded in the "Access Token" field).
2. In the left panel titled **Access Token Info**, find the clickable blue "App ID" row, or even better, the **Page ID** row that appears when you generate a Page Token.
3. If you don't see it, in the top query field (where it says `GET v18.0 /`) simply type `me` and click **Submit**.
4. The JSON response on the right will look like:
   ```json
   {
     "name": "Your Page Name",
     "id": "123456789012345"
   }
   ```
5. That number `123456789012345` is your **`FACEBOOK_PAGE_ID`**. Copy it and paste it into the `.env` file.
6. Now change the query field at the top to: `{YOUR_PAGE_ID}?fields=instagram_business_account` (replace the bracketed part with the number you just copied) and click **Submit** again.
7. The response will change to:
   ```json
   {
     "instagram_business_account": {
       "id": "987654321098765"
     },
     "id": "123456789012345"
   }
   ```
8. That new number under `instagram_business_account` (e.g., `987654321098765`) is your **`INSTAGRAM_ACCOUNT_ID`**. Copy it and save it in the `.env` file.

## Part 3: Configuring Threads API

If you also want to post to Threads, you must add the related product. In "Business" Apps, Threads might be located in a different section than the main panels.

1. From the left menu, click on **Use Cases** (if present) or search for Threads among the Products.
2. If using "Use Cases", select the option to customize permissions and click *Add*. Search for **Threads API**.
3. In the Threads specific settings (if displayed), add `https://localhost` or your local development URL to the **Valid OAuth Redirect URIs**.
4. You can request the token for Threads directly from the Graph API Explorer using the same steps as Instagram, but asking for `threads_basic` and `threads_content_publish` permissions.

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
