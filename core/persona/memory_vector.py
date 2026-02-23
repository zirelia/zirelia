# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
import time
import os
from config.settings import get_settings
from core.utils.logger import logger

settings = get_settings()

class VectorMemory:
    def __init__(self, persistence_path: str = "./memory_db"):
        self.client = chromadb.PersistentClient(path=persistence_path)
        
        # Use OpenAI Embeddings if key is present, otherwise default (sentence-transformers)
        if settings.OPENAI_API_KEY:
            self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )
        else:
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            
        self.collection = self.client.get_or_create_collection(
            name="persona_memory",
            embedding_function=self.embedding_fn
        )
        logger.info(f"VectorMemory initialized at {persistence_path}")

    def add_memory(self, text: str, metadata: Dict[str, Any] = None):
        """Adds a memory to the vector store."""
        try:
            self.collection.add(
                documents=[text],
                metadatas=[metadata or {}],
                ids=[str(hash(text + str(time.time())))] # Simple unique ID
            )
            logger.debug(f"Memory added: {text[:50]}...")
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")

    def search_memory(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieves relevant memories."""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"Memory search failed: {e}")
            return []

import time
