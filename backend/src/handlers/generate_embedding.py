"""
Generate Embedding Handler

Generates taste embedding vector using Titan v2.
Uses caching to avoid redundant API calls.
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

from ..services.bedrock_client import TitanService
from ..services.cache_service import CacheService
from ..services.dynamodb_client import DynamoDBClient
from ..utils.embedding_builder import (
    build_embedding_document,
    compute_document_hash,
    format_answers_for_storage
)
from ..utils.vector_ops import normalize_vector, validate_vector
from ..utils.validation import validate_user_id, validate_section1_answers, validate_section2_answers

logger = logging.getLogger(__name__)


def generate_embedding(
    user_id: str,
    section1_answers: List[Dict[str, Any]],
    section2_answers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate taste embedding vector.
    
    Args:
        user_id: User identifier
        section1_answers: Section 1 answers
        section2_answers: Section 2 answers
        
    Returns:
        Dictionary with embeddingId and vector
        
    Raises:
        ValueError: If inputs invalid
        Exception: If generation fails
    """
    try:
        # Validate inputs
        validate_user_id(user_id)
        validate_section1_answers(section1_answers)
        validate_section2_answers(section2_answers)
        
        # Initialize services
        titan = TitanService()
        cache = CacheService()
        db = DynamoDBClient()
        
        logger.info(f"Generating embedding for user {user_id}")
        
        # Build embedding document
        document = build_embedding_document(section1_answers, section2_answers)
        doc_hash = compute_document_hash(document)
        
        logger.info(f"Document hash: {doc_hash[:16]}...")
        
        # Try cache first, generate if miss
        def generate_new_embedding():
            logger.info("Calling Titan to generate embedding...")
            return titan.embed_text(document, normalize=True)
        
        embedding, was_cached = cache.get_or_generate(
            document,
            generate_new_embedding,
            metadata={
                "userId": user_id,
                "documentLength": len(document)
            }
        )
        
        if was_cached:
            logger.info("Using cached embedding")
        else:
            logger.info("Generated new embedding")
        
        # Validate embedding
        validate_vector(embedding, expected_dim=1024, check_normalized=True)
        
        # Store embedding in Users table (NOT raw answers)
        formatted_answers = format_answers_for_storage(section1_answers, section2_answers)
        
        user_data = {
            "userId": user_id,
            "embedding": embedding,
            "embeddingHash": doc_hash,
            "answerMetadata": formatted_answers,  # Only metadata, not raw answers
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }
        
        # Check if user exists
        existing_user = db.get_user(user_id)
        if existing_user:
            # Update existing user
            db.update(
                table_name=db.users_table,
                key={"userId": user_id},
                update_expression=(
                    "SET embedding = :emb, "
                    "embeddingHash = :hash, "
                    "answerMetadata = :meta, "
                    "updatedAt = :timestamp"
                ),
                expression_values={
                    ":emb": embedding,
                    ":hash": doc_hash,
                    ":meta": formatted_answers,
                    ":timestamp": datetime.utcnow().isoformat()
                }
            )
        else:
            # Create new user
            db.put_user(user_data)
        
        logger.info(f"Embedding stored for user {user_id}")
        
        return {
            "embeddingId": doc_hash,
            "embedding": embedding,
            "cached": was_cached
        }
        
    except Exception as e:
        logger.error(f"Error generating embedding: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    test_s1 = [
        {"questionId": f"q{i}", "selectedOptions": ["opt"], "category": "test"}
        for i in range(1, 6)
    ]
    test_s2 = [
        {"questionId": f"q{i}", "selectedOptions": ["opt"], "category": "test"}
        for i in range(6, 11)
    ]
    
    # result = generate_embedding("test-user", test_s1, test_s2)
    # print(f"Generated embedding: {len(result['embedding'])} dimensions")
