# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import os
from celery import Celery
import time

# Initialize Celery
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery("tasks", broker=redis_url, backend=redis_url)

from virtual_influencer_engine.database.db import SessionLocal
from virtual_influencer_engine.database.models import Post, Analytics
from virtual_influencer_engine.core.persona.engine import PersonaEngine
from virtual_influencer_engine.core.image_gen.pipeline import ImageGenerator
from virtual_influencer_engine.core.content.generator import ContentGenerator
from virtual_influencer_engine.core.social.platforms import PlatformFactory

@celery.task(name="generate_content_task")
def generate_content_task(platform: str, topic: str):
    """
    Background task to generate content.
    """
    print(f"[Worker] Starting content generation for {platform} on topic '{topic}'")

    # Initialize Engines
    persona_engine = PersonaEngine()
    content_generator = ContentGenerator(persona_engine)
    image_generator = ImageGenerator()

    # 1. Generate Image
    image_path = image_generator.generate_image(f"{topic}", style="lifestyle")

    # 2. Generate Caption
    caption = content_generator.generate_caption(platform, topic)

    # 3. Save to DB
    db = SessionLocal()
    try:
        new_post = Post(
            platform=platform,
            content=caption,
            image_path=image_path,
            status="draft"
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        print(f"[Worker] Content generated and saved with ID: {new_post.id}")
        return {"status": "success", "post_id": new_post.id}
    finally:
        db.close()

@celery.task(name="post_content_task")
def post_content_task(post_id: int):
    """
    Background task to post content.
    """
    print(f"[Worker] Posting content for post_id {post_id}")

    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return {"status": "error", "message": "Post not found"}

        manager = PlatformFactory.get_platform(post.platform, config={})
        result = manager.post_content(post.content, post.image_path)

        if result.get("status") == "success":
            post.status = "published"
            analytics = Analytics(post_id=post.id)
            db.add(analytics)
            db.commit()
            print(f"[Worker] Post {post_id} published successfully.")
            return {"status": "success", "platform_response": result}
        else:
            print(f"[Worker] Failed to publish post {post_id}: {result}")
            return {"status": "error", "message": "Failed to publish"}
    except Exception as e:
        print(f"[Worker] Error: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
