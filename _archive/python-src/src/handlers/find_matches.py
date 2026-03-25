"""
Find Matches Handler

This module handles finding taste matches using cosine similarity on embedding vectors.
"""

import logging
from typing import Dict, Any, List

from ..services.dynamodb_client import get_dynamodb_client
from ..utils.vector_ops import cosine_similarity

logger = logging.getLogger(__name__)


def find_matches(user_id: str, limit: int = 10) -> Dict[str, Any]:
    """
    Find taste matches for user based on embedding similarity.
    
    Calculates cosine similarity with all other users and returns top matches.
    
    Args:
        user_id: User identifier
        limit: Maximum number of matches to return (1-50)
        
    Returns:
        Dictionary with list of matches
        
    Raises:
        Exception: If user not found or matching fails
    """
    try:
        logger.info(f"Finding matches for user: {user_id}, limit: {limit}")
        
        # Validate limit
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50")
        
        # Retrieve user's embedding vector
        dynamodb = get_dynamodb_client()
        user = dynamodb.get_item('Users', {'userId': user_id})
        
        if not user:
            raise Exception("User not found")
        
        user_vector = user.get('vector')
        if not user_vector:
            raise Exception("User embedding not found")
        
        # Get all users
        all_users = dynamodb.scan('Users')
        
        # Calculate similarity with each user
        matches = []
        for other_user in all_users:
            other_user_id = other_user.get('userId')
            
            # Skip self
            if other_user_id == user_id:
                continue
            
            # Skip users without embeddings
            other_vector = other_user.get('vector')
            if not other_vector:
                continue
            
            # Calculate cosine similarity
            similarity = cosine_similarity(user_vector, other_vector)
            
            # Only include matches above threshold
            if similarity > 0.7:
                # Find shared traits
                shared_traits = _find_shared_traits(
                    user.get('tasteDNA', {}),
                    other_user.get('tasteDNA', {})
                )
                
                match = {
                    'userId': other_user_id,
                    'username': other_user.get('username', 'Anonymous'),
                    'similarity': round(similarity, 3),
                    'sharedTraits': shared_traits,
                    'archetype': other_user.get('tasteDNA', {}).get('archetype', 'Unknown')
                }
                
                matches.append(match)
        
        # Sort by similarity descending
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Limit results
        matches = matches[:limit]
        
        logger.info(f"Found {len(matches)} matches for user: {user_id}")
        
        return {'matches': matches}
        
    except Exception as e:
        logger.error(f"Failed to find matches: {str(e)}", exc_info=True)
        raise


def _find_shared_traits(dna1: Dict[str, Any], dna2: Dict[str, Any]) -> List[str]:
    """
    Find shared traits between two DNA profiles.
    
    Identifies traits that both users have with similar scores.
    
    Args:
        dna1: First user's DNA profile
        dna2: Second user's DNA profile
        
    Returns:
        List of shared trait names
    """
    shared = []
    
    traits1 = {t['name']: t['score'] for t in dna1.get('traits', [])}
    traits2 = {t['name']: t['score'] for t in dna2.get('traits', [])}
    
    # Find traits present in both with similar scores (within 2 points)
    for trait_name, score1 in traits1.items():
        if trait_name in traits2:
            score2 = traits2[trait_name]
            if abs(score1 - score2) <= 2.0:
                shared.append(trait_name)
    
    return shared
