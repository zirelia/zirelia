# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database.db import get_db, engine, Base
from ..database.models import Post, Analytics
from ..core.persona.engine import PersonaEngine
from ..core.content.generator import ContentGenerator
from ..core.image_gen.pipeline import ImageGenerator
from ..core.social.platforms import PlatformFactory
from ..workers.tasks import generate_content_task, post_content_task

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Virtual Influencer Engine")

# Pydantic Models
class PostCreateRequest(BaseModel):
    platform: str
    topic: str
    style: Optional[str] = "lifestyle"

class PostResponse(BaseModel):
    id: Optional[int]
    platform: str
    content: Optional[str]
    image_path: Optional[str]
    status: str

@app.post("/generate", status_code=202)
def generate_post(request: PostCreateRequest):
    """
    Triggers a background task to generate a post (image + caption) for a specific platform.
    """
    # Trigger Celery Task
    task = generate_content_task.delay(request.platform, request.topic)

    return {"message": "Generation started", "task_id": task.id}

@app.post("/publish/{post_id}", status_code=202)
def publish_post(post_id: int, db: Session = Depends(get_db)):
    """
    Triggers a background task to publish a drafted post.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.status == "published":
        return {"message": "Post already published"}

    # Trigger Celery Task
    task = post_content_task.delay(post_id)

    return {"message": "Publishing started", "task_id": task.id}

@app.get("/posts", response_model=List[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return [
        PostResponse(
            id=p.id,
            platform=p.platform,
            content=p.content,
            image_path=p.image_path,
            status=p.status
        ) for p in posts
    ]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Virtual Influencer Engine API"}
