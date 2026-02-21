# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license


import os
from dotenv import load_dotenv
import tweepy

# Load environment variables
load_dotenv()

def check_read_access():
    print("Locked & Loaded. Testing Twitter Read Access... 🕵️‍♂️")

    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("❌ Missing API Keys in .env")
        return

    try:
        # Initialize Client
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token
        )

        # 1. Try to get own user ID (Read User)
        print("\nStep 1: Fetching My User ID...")
        me = client.get_me()
        if not me.data:
            print("❌ Failed to fetch user data.")
            return
        
        user_id = me.data.id
        username = me.data.username
        print(f"✅ Success! User: @{username} (ID: {user_id})")

        # 2. Try to fetch Mentions (Read Tweets)
        print(f"\nStep 2: Checking Mentions for user {user_id}...")
        try:
            mentions = client.get_users_mentions(id=user_id, max_results=5)
            print("✅ SUCCESS! Read Access Confirmed.")
            if mentions.data:
                print(f"   Found {len(mentions.data)} mentions.")
                for m in mentions.data:
                    print(f"   - {m.text[:50]}...")
            else:
                print("   (No mentions found, but access works)")

        except tweepy.errors.Forbidden as e:
            print(f"❌ 403 FORBIDDEN: You do not have Read Access for Tweets/Mentions.")
            print(f"   Reason: {e}")
            print("   👉 Likely restricted to 'Write Only' on Free/Metered Tier.")
            
        except Exception as e:
            print(f"❌ Error fetching mentions: {e}")

    except Exception as e:
        print(f"❌ Fatal Error initializing client: {e}")

if __name__ == "__main__":
    check_read_access()
