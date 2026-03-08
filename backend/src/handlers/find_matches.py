"""
Find Matches Handler

Finds users with similar taste profiles using cosine similarity.
"""

import logging
from typing import Dict, List, Any, Optional

from ..services.dynamodb_client import DynamoDBClient
from ..utils.vector_ops import cosine_similarity
from ..utils.validation import validate_user_id

logger = logging.getLogger(__name__)


def find_matches(
    user_id: str,
    limit: int = 10,
    min_similarity: float = 0.7
) -> List[Dict[str, Any]]:
    """
    Find taste matches for user.
    
    Args:
        user_id: User identifier
        limit: Maximum number of matches to return (1-50)
        min_similarity: Minimum similarity threshold (0.0-1.0)
        
    Returns:
        List of matches sorted by similarity (descending)
        
    Raises:
        ValueError: If user not found or no embedding
        Exception: If matching fails
    """
    try:
        validate_user_id(user_id)
        
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50")
        
        if min_similarity < 0.0 or min_similarity > 1.0:
            raise ValueError("Min similarity must be between 0.0 and 1.0")
        
        db = DynamoDBClient()
        
        logger.info(f"Finding matches for user {user_id}")
        
        # Get user's embedding
        user = db.get_user(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
        
        user_embedding = user.get("embedding")
        if not user_embedding:
            raise ValueError(f"User {user_id} has no embedding")
        
        # Scan all users (exclude requesting user)
        all_users = db.scan_users()
        
        matches = []
        for other_user in all_users:
            other_id = other_user.get("userId")
            
            # Skip self
            if other_id == user_id:
                continue
            
            other_embedding = other_user.get("embedding")
            if not other_embedding:
                continue
            
            # Calculate similarity
            try:
                similarity = cosine_similarity(user_embedding, other_embedding)
            except Exception as e:
                logger.warning(f"Failed to calculate similarity with {other_id}: {e}")
                continue
            
            # Filter by threshold
            if similarity < min_similarity:
                continue
            
            # Identify shared traits
            shared_traits = _identify_shared_traits(
                user.get("tasteDNA", {}),
                other_user.get("tasteDNA", {})
            )
            
            matches.append({
                "userId": other_id,
                "similarity": round(similarity, 4),
                "tasteDNA": other_user.get("tasteDNA", {}),
                "sharedTraits": shared_traits
            })
        
        # Sort by similarity (descending)
        matches.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Limit results
        matches = matches[:limit]
        
        logger.info(f"Found {len(matches)} matches for user {user_id}")
        
        return matches
        
    except Exception as e:
        logger.error(f"Error finding matches: {e}", exc_info=True)
        raise


def _identify_shared_traits(
    dna1: Dict[str, Any],
    dna2: Dict[str, Any]
) -> List[str]:
    """
    Identify shared traits between two DNA profiles.
    
    Args:
        dna1: First DNA profile
        dna2: Second DNA profile
        
    Returns:
        List of shared trait names
    """
    shared = []
    
    traits1 = {t.get("name"): t.get("score", 0) for t in dna1.get("traits", [])}
    traits2 = {t.get("name"): t.get("score", 0) for t in dna2.get("traits", [])}
    
    # Find traits that appear in both with similar scores
    for trait_name in traits1:
        if trait_name in traits2:
            score1 = traits1[trait_name]
            score2 = traits2[trait_name]
            
            # Consider shared if scores are within 2 points
            if abs(score1 - score2) <= 2.0:
                shared.append(trait_name)
    
    return shared


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    
    # result = find_matches("test-user", limit=5)
    # print(f"Found {len(result)} matches")
