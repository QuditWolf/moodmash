"""
Generate Embedding Handler

This module handles embedding generation from quiz answers using Titan v2.
Implements caching and privacy-first storage (no raw answers stored).
"""

import logging
import time
import uuid
from typing import Dict, Any, List

from ..services.bedrock_client import get_titan_service
from ..services.cache_service import get_cache_service
from ..services.dynamodb_client import get_dynamodb_client
from ..utils.embedding_builder import build_embedding_document, apply_weights
from ..utils.vector_ops import normalize_vector

logger = logging.getLogger(__name__)


def generate_embedding(
    session_id: str,
    user_id: str,
    all_answers: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate embedding vector from quiz answers.
    
    Builds embedding document, checks cache, generates vector with Titan v2,
    applies weighting, normalizes, and stores in Users table.
    
    Args:
        session_id: Session identifier
        user_id: User identifier
        all_answers: Dictionary with section1 and section2 answers
        
    Returns:
        Dictionary with embeddingId and vector
        
    Raises:
        Exception: If embedding generation fails
    """
    try:
        logger.info(f"Generating embedding for user: {user_id}, session: {session_id}")
        
        # Build embedding document from quiz answers
        document = build_embedding_document(all_answers)
        logger.info(f"Built embedding document ({len(document)} chars)")
        
        # Check cache for existing embedding
        cache = get_cache_service()
        cached_vector = cache.get(document)
        
        if cached_vector:
            # Cache hit - use cached vector
            logger.info("Using cached embedding vector")
            vector = cached_vector
        else:
            # Cache miss - generate new embedding with Titan
            logger.info("Cache miss - generating new embedding with Titan")
            titan = get_titan_service()
            vector = titan.generate_embedding(
                text=document,
                dimensions=1024,
                normalize=True
            )
            
            # Store in cache for future use
            cache.put(document, vector)
        
        # Apply weighting engine
        weighted_vector = apply_weights(vector, all_answers)
        
        # Normalize weighted vector to unit length
        normalized_vector = normalize_vector(weighted_vector)
        
        # Generate embedding ID
        embedding_id = str(uuid.uuid4())
        
        # Store in Users table (NOT raw answers - privacy first!)
        dynamodb = get_dynamodb_client()
        timestamp = int(time.time())
        
        user_record = {
            'userId': user_id,
            'embeddingId': embedding_id,
            'vector': normalized_vector,
            'dimension': 1024,
            'createdAt': timestamp,
            'updatedAt': timestamp,
            'quizVersion': 'v1'
        }
        
        dynamodb.put_item('Users', user_record)
        
        logger.info(f"Embedding stored successfully: {embedding_id}")
        
        return {
            'embeddingId': embedding_id,
            'vector': normalized_vector,
            'dimension': 1024
        }
        
    except Exception as e:
        logger.error(f"Failed to generate embedding: {str(e)}", exc_info=True)
        raise Exception("Failed to generate taste profile")
