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
    > ⚠️ **DO NOT add Threads permissions here!** Threads requires a **completely separate** Meta App with its own OAuth flow. See **Part 4** of this guide.
6. Click the giant green button **Generate Access Token** and re-confirm the Facebook popup.
7. WE ARE CLOSE: Return to the **User or Page** dropdown and open it. Click on the **Name of your Page** (e.g., "Sienna Fox").
8. The long string in the center of the screen will change: **that is your Page Token**! Copy it somewhere safe.

### Making the Token TEMPORARY -> PERMANENT (Never Expires)

The default token expires after 1 hour. Extending it normally makes it last 60 days. But for an autonomous bot, you must generate a **Permanent Page Access Token**:

1. Still in the Graph API Explorer (with your short-lived *User* Token already loaded), click the small blue exclamation mark (ℹ️) next to the token string.
2. Click **Open in Access Token Tool**.
3. At the bottom of the tool page, click **Extend Access Token**.
4. This generates a 60-day User token. **Copy this 60-day token.**
5. Now return to the main Graph API Explorer page.
6. **Paste the 60-day token** into the "Access Token" field (overwriting the old one).
7. In the API URL bar (where it says `GET v26.0 /`), delete everything and type: `me/accounts`
8. Click **Submit**.
9. In the black box on the right, you will see a list of your Pages. Under your Page name (e.g., Sienna Fox), you will see an `access_token` field with a very long string.
10. **THAT TOKEN IS PERMANENT!** You can verify this by pasting it into the Access Token Debugger: the Expiration will say "Never".

**Copy this permanent token.** This will be your `META_ACCESS_TOKEN` in the `.env` file, and your bot will never stop working.

### Finding your IDs (Facebook Page ID and Instagram Account ID)

To make the posting script work (and paste them into your `.env` file), Zirelia needs to know exactly the ID of the bridge Page and the ID of the Instagram profile. The Graph API Explorer offers the simplest way without struggling with JSON parsing:

1. Go back to the **Graph API Explorer** (ensure your Page Token is still loaded in the "Access Token" field).
2. In the left panel titled **Access Token Info**, find the clickable blue "App ID" row, or even better, the **Page ID** row that appears when you generate a Page Token.
3. If you don't see it, in the top query field (where it says `GET v26.0 /`) simply type `me` and click **Submit**.
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

---

## Part 4: Configuring the Threads API (Separate App!)

> [!CAUTION]
> Threads is **NOT** a "product" you can add to the existing Business App (the one used for Facebook and Instagram). Threads requires the creation of a **brand new, separate app** with a dedicated Use Case. The token and API endpoint are also completely different.

> [!IMPORTANT]
> **TWO DIFFERENT ACCOUNTS — DON'T MIX THEM UP!**
> Throughout this process you'll use **two different accounts**:
> - **Admin Account** (e.g., `lantoniotrento`): your personal Facebook account that manages apps on the Developer Portal.
> - **Target Account** (e.g., `itssiennafox`): your AI's Threads account, where content will be published.
>
> Each step specifies which account to use.

### 4.1 Creating the Threads App

*👤 Use your **Admin Account** on the Developer Portal.*

1. Go to [developers.facebook.com/apps/](https://developers.facebook.com/apps/).
2. Click **Create App**.
3. On the **Use Cases** screen, select **"Access the Threads API"** and click Next.
4. Give the app a name (e.g., "Zirelia Threads"). Click **Create App**.

### 4.2 Configuring the App (URLs + Permissions)

*👤 Use your **Admin Account** on the Developer Portal.*

Go to **Use Cases → Access the Threads API → Customize**. This page contains everything: credentials, URLs, and permissions.

**① Note the credentials** (in the top section of the page):

| Field on the Customize page | What it is | Where it's needed |
|---|---|---|
| **Threads App ID** | The `client_id` for OAuth | OAuth URL and curl commands |
| **Threads App Secret** | The `client_secret` | Curl commands and `.env` as `THREADS_APP_SECRET` |

> [!WARNING]
> The **"Threads App ID"** on the Customize page is **DIFFERENT** from the App ID shown in Settings > Basic! For the OAuth URL, you must use the one from the **Customize** page.

**② Fill in ALL mandatory URL fields** with the same HTTPS URL:

> [!CAUTION]
> **`https://localhost/` DOES NOT WORK!** Meta rejects `localhost` as a redirect URI for Threads apps. Use a real HTTPS URL.

> [!WARNING]
> **BEWARE OF AUTOMATIC REDIRECTS**: If your site has an automatic redirect (e.g., from `/` to `/it/`), the `code` parameter will be lost! Use a path that **doesn't redirect** (e.g., `https://your-site.github.io/callback`) — a 404 page is fine, what matters is that the URL stays visible in the address bar with the `?code=` parameter.

| Field | Value |
|---|---|
| **Redirect callback URL** | `https://your-site.github.io/callback` |
| **Deauthorize callback URL** | `https://your-site.github.io/callback` |
| **Delete callback URL** | `https://your-site.github.io/callback` |

**③ Enable mandatory permissions** (in the "Permissions and features" section):
- `threads_basic` (required)
- `threads_content_publish` (required)
- Optional: `threads_manage_replies`, `threads_read_replies`, `threads_manage_insights`

Click **Save**.

### 4.3 Adding the Target Account as a Tester

*👤 Steps 1-3 with **Admin Account**, steps 4-6 with **Target Account**.*

While the app is in Development mode (indicated by "Not published" in the sidebar menu), only users added as "Testers" can authorize the app.

**From the Developer Portal (Admin Account):**
1. In the sidebar menu, go to **App Roles → Roles**.
2. Click **Add People** and select **Threads Tester**.
3. Enter the **Threads username of the Target Account** (e.g., `itssiennafox` — without the @).

**From the Threads app on your phone (Target Account):**
4. Log into the **Threads** app on your phone with the **Target Account**.
5. Go to **☰ → Settings and privacy → Account → Website permissions → Invites**.
6. Accept the invitation from your app.

> [!TIP]
> If you can't find "Website permissions", try: **Settings → Privacy → App invitations**. The interface changes frequently. If the Target profile is private, make it **public** first.

### 4.4 Generating the Threads Token

There are **two methods**. Try Method A first (simpler).

#### Method A: Token Generator from the Dashboard (Recommended)

*👤 Use your **Admin Account** on the Developer Portal.*

1. Go to **Use Cases → Access the Threads API → Customize**.
2. Scroll down to the **"User Token Generator"** section at the bottom of the page.
3. Next to your tester name (e.g., itssiennafox) there should be a **"Generate token"** button.
4. Click to generate a **long-lived token** directly — no manual OAuth flow needed!
5. Copy the token and add it to `.env` as `THREADS_ACCESS_TOKEN`.

> 💡 If the button doesn't appear or gives an error, use Method B.

#### Method B: Manual OAuth Flow

> [!WARNING]
> You must be logged into Threads as the **TARGET Account** (e.g., itssiennafox), **NOT** as the admin account!

**Step 1** — Open this URL in your browser (replace values with those from the Customize page in step 4.2):

```
https://threads.net/oauth/authorize?client_id={THREADS_APP_ID}&redirect_uri={YOUR_REDIRECT_URI}&scope=threads_basic,threads_content_publish&response_type=code
```

**Step 2** — Authorize the app (logged in as the Target Account).

**Step 3** — The browser will take you to your redirect URI with `?code=ABC123...#_` in the address bar. **Copy the part after `?code=` and before `#_`**.

**Step 4** — Exchange the code for a short-lived token (from PowerShell):

```bash
curl -X POST "https://graph.threads.net/oauth/access_token" \
  -d "client_id={THREADS_APP_ID}" \
  -d "client_secret={THREADS_APP_SECRET}" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri={YOUR_REDIRECT_URI}" \
  -d "code={THE_COPIED_CODE}"
```

> [!WARNING]
> The `redirect_uri` must be **identical** to the one set in step 4.2 (including the trailing `/`).

**Step 5** — The response will contain `access_token` and `user_id`. Save both! The `user_id` is your `THREADS_USER_ID`.

**Step 6** — Exchange the short-lived token for a **long-lived token** (60 days):

```bash
curl -s "https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret={THREADS_APP_SECRET}&access_token={SHORT_LIVED_TOKEN}"
```

**Step 7** — The returned token is your **`THREADS_ACCESS_TOKEN`**. Copy it into `.env`.

### 4.5 Token Renewal (60 days)

> [!WARNING]
> **The Threads token is NOT permanent!** It lasts **60 days** and must be renewed. To renew it before expiration:
> ```bash
> curl -s "https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={YOUR_CURRENT_TOKEN}"
> ```
> A good approach is to set up a cron job that renews the token every 50 days.

### 4.6 Finding the Threads User ID

If you didn't save it during token creation, you can retrieve it:

```bash
curl -s "https://graph.threads.net/v1.0/me?access_token={THREADS_ACCESS_TOKEN}"
```

The response will contain `"id": "123456789"` — that is your `THREADS_USER_ID`.

---

## Part 5: Credentials Summary

At the end of the process, you should have these credentials in your `.env` file:

**From the Business App** (Facebook & Instagram):

```env
# Meta / Instagram Settings (from the Business App)
META_APP_ID=your_app_id_from_dashboard
META_APP_SECRET=your_app_secret_from_dashboard
META_ACCESS_TOKEN=your_permanent_page_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
INSTAGRAM_ACCOUNT_ID=your_instagram_business_account_id
```

**From the separate Threads App** (Use Case "Access the Threads API"):

```env
# Threads Settings (from the SEPARATE Threads App)
THREADS_APP_SECRET=your_threads_app_secret
THREADS_ACCESS_TOKEN=your_long_lived_threads_token_60_days
THREADS_USER_ID=your_threads_user_id
```

### Important Notes for Production

*   **Token Expiration (Facebook/Instagram)**: If you correctly followed the steps to obtain a **Permanent Page Access Token**, it will **never expire**. It works indefinitely unless you change your Facebook password or manually revoke the App's access from your settings.
*   **Token Expiration (Threads)**: The Threads token lasts **60 days** and must be renewed. You can use the `refresh_access_token` endpoint to extend it by another 60 days. If it expires, you must repeat the OAuth flow. A good approach is to set up a cron job that renews the token every 50 days.
*   **App Review**: While you are the only user of the apps (Admin/Tester role), **neither** app needs to be submitted for Meta App Review. Both can remain in **"Development"** mode indefinitely. They will remain private and 100% functional for your own linked accounts.
