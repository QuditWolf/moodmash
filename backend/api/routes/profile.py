"""
Profile API Routes

Handles user profile data:
- Taste DNA retrieval
- Growth path recommendations
- Taste matches
- Behavioral analytics
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["profile"])


# Response Models
class TasteDNAResponse(BaseModel):
    tasteDNA: Dict[str, Any]


class GrowthPathResponse(BaseModel):
    path: Dict[str, Any]


class Match(BaseModel):
    userId: str
    similarity: float
    tasteDNA: Dict[str, Any]
    sharedTraits: List[str]


class MatchesResponse(BaseModel):
    matches: List[Match]


class AnalyticsResponse(BaseModel):
    analytics: Dict[str, Any]


class DNACardResponse(BaseModel):
    imageId: str
    imageData: str  # base64 encoded image
    format: str
    width: int
    height: int
    model: str
    userId: str
    archetype: str


@router.get("/dna/{user_id}", response_model=TasteDNAResponse)
async def get_taste_dna(user_id: str):
    """
    Get user's taste DNA profile.
    
    Args:
        user_id: User identifier
        
    Returns:
        Taste DNA with archetype, traits, and categories
    """
    try:
        logger.info(f"Fetching taste DNA for user {user_id}")
        
        # TODO: Retrieve from DynamoDB Users table
        
        # Mock response
        taste_dna = {
            "archetype": "The Curator",
            "description": "You have a refined eye for quality and meaning.",
            "traits": [
                {
                    "name": "Aesthetic Sensitivity",
                    "score": 0.85,
                    "description": "Strong appreciation for visual beauty"
                }
            ],
            "categories": {
                "visual": ["minimalist", "contemporary"],
                "mood": ["reflective", "inspiring"],
                "engagement": ["observe", "curate"]
            }
        }
        
        return TasteDNAResponse(tasteDNA=taste_dna)
        
    except Exception as e:
        logger.error(f"Error fetching taste DNA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/path/{user_id}", response_model=GrowthPathResponse)
async def get_growth_path(user_id: str):
    """
    Get user's personalized growth path.
    
    Args:
        user_id: User identifier
        
    Returns:
        Growth path with Absorb/Create/Reflect recommendations
    """
    try:
        logger.info(f"Fetching growth path for user {user_id}")
        
        # Import handler
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.handlers.generate_path import generate_path
        
        # Generate or retrieve path
        path = generate_path(user_id)
        
        return GrowthPathResponse(path=path)
        
    except Exception as e:
        logger.error(f"Error fetching growth path: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matches/{user_id}", response_model=MatchesResponse)
async def get_matches(
    user_id: str,
    limit: int = Query(default=10, ge=1, le=50)
):
    """
    Get taste matches for user.
    
    Args:
        user_id: User identifier
        limit: Maximum number of matches (1-50)
        
    Returns:
        List of users with similar taste profiles
    """
    try:
        logger.info(f"Fetching matches for user {user_id}, limit={limit}")
        
        # Import handler
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.handlers.find_matches import find_matches
        
        # Find matches
        matches = find_matches(user_id, limit=limit)
        
        return MatchesResponse(matches=matches)
        
    except Exception as e:
        logger.error(f"Error fetching matches: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/{user_id}", response_model=AnalyticsResponse)
async def get_analytics(user_id: str):
    """
    Get behavioral analytics for user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Analytics with insights and patterns
    """
    try:
        logger.info(f"Fetching analytics for user {user_id}")
        
        # Import handler
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.handlers.generate_analytics import generate_analytics
        
        # Generate analytics
        analytics = generate_analytics(user_id)
        
        return AnalyticsResponse(analytics=analytics)
        
    except Exception as e:
        logger.error(f"Error fetching analytics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dna-card/{user_id}", response_model=DNACardResponse)
async def generate_dna_card_image(
    user_id: str,
    model: str = Query(default="titan", regex="^(titan|nova|sdxl)$"),
    width: int = Query(default=1024, ge=512, le=1536),
    height: int = Query(default=1024, ge=512, le=1536)
):
    """
    Generate visual DNA card image for user.
    
    This endpoint creates a highly detailed digital collage "Taste DNA Card"
    that visually represents the user's cultural taste identity.
    
    Args:
        user_id: User identifier
        model: Image generation model ('titan', 'nova', or 'sdxl')
        width: Image width in pixels (512-1536)
        height: Image height in pixels (512-1536)
        
    Returns:
        DNA card image data (base64 encoded) and metadata
        
    Note:
        This requires AWS Bedrock access with image generation models enabled.
        Supported models:
        - titan: Amazon Titan Image Generator v2 (fast, good quality)
        - nova: Amazon Nova Canvas (high quality, flexible)
        - sdxl: Stability AI Stable Diffusion XL (slower, highest quality)
    """
    try:
        logger.info(f"Generating DNA card image for user {user_id} with model {model}")
        
        # Import handler
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.handlers.generate_dna_card import generate_dna_card
        
        # Generate DNA card image
        result = generate_dna_card(
            user_id=user_id,
            model=model,
            width=width,
            height=height
        )
        
        return DNACardResponse(**result)
        
    except ValueError as e:
        # User not found or missing DNA profile
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating DNA card: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
