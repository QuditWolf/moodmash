"""
Generate DNA Card Image Handler

Generates a visual "Taste DNA Card" image using AWS Bedrock image generation.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from ..services.dynamodb_client import DynamoDBClient
from ..services.image_generation_client import ImageGenerationClient

logger = logging.getLogger(__name__)


def load_prompt_template(prompt_file: str) -> str:
    """Load prompt template from file."""
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "prompts",
        prompt_file
    )
    with open(prompt_path, 'r') as f:
        return f.read()


def build_dna_card_prompt(
    username: str,
    archetype: str,
    summary: str,
    tastes: list,
    traits: Optional[Dict[str, int]] = None
) -> str:
    """
    Build the DNA card image generation prompt.
    
    Args:
        username: User's display name
        archetype: DNA archetype name
        summary: Vibe summary text
        tastes: List of taste signals (strings)
        traits: Optional trait scores (e.g., {"Music": 92, "Literature": 88})
        
    Returns:
        Complete prompt for image generation
    """
    # Create a very concise prompt (Titan v2 has 512 char limit)
    tastes_str = ", ".join(tastes[:5]) if isinstance(tastes, list) else str(tastes)  # Limit to 5 tastes
    
    # Ultra-short prompt under 512 chars
    prompt = f"""Digital collage art poster: "{username}" - {archetype}. Layered indie zine aesthetic, torn paper, stickers, glitch art. Surreal background with {tastes_str}. Young creative avatar with headphones. Typography: {username}, {archetype}. Moodmash DNA helix logo. Cinematic lighting, poster-quality, detailed textures, modern graphic design."""
    
    # Ensure under 512 chars
    if len(prompt) > 500:
        prompt = f"""Collage art poster: {username} - {archetype}. Indie zine style, torn paper, glitch art. Avatar with headphones. {tastes_str[:100]}. Moodmash logo. Detailed, cinematic."""
    
    return prompt


def generate_dna_card(
    user_id: str,
    model: str = "titan",
    width: int = 1024,
    height: int = 1024
) -> Dict[str, Any]:
    """
    Generate DNA card image for a user.
    
    Args:
        user_id: User ID
        model: Image generation model ('titan' or 'sdxl')
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        Dictionary with imageId, imageData (base64), and metadata
        
    Raises:
        Exception: If generation fails or user not found
    """
    try:
        # Initialize services
        db = DynamoDBClient()
        image_gen = ImageGenerationClient()
        
        logger.info(f"Generating DNA card for user {user_id}")
        
        # Retrieve user data
        user = db.get_user(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
        
        # Extract DNA profile
        dna_profile = user.get("tasteDNA")
        if not dna_profile:
            raise ValueError(f"User {user_id} does not have a DNA profile")
        
        # Extract required fields
        username = user.get("username", user_id)
        archetype = dna_profile.get("archetype", "Cultural Explorer")
        summary = dna_profile.get("description", "A unique taste profile")
        
        # Extract tastes from DNA profile
        # Tastes can come from categories or traits
        tastes = []
        
        # Get from categories
        categories = dna_profile.get("categories", {})
        for category, items in categories.items():
            if isinstance(items, list):
                tastes.extend(items[:3])  # Take top 3 from each category
        
        # Get from traits if available (traits is a list of dicts, not a dict)
        traits_list = dna_profile.get("traits", [])
        traits_data = {}
        if isinstance(traits_list, list):
            for trait in traits_list:
                if isinstance(trait, dict):
                    name = trait.get("name", "")
                    score = trait.get("score", 0)
                    if name and score:
                        traits_data[name] = int(score * 10)  # Convert 0-10 to 0-100
        
        # If no tastes found, use a default
        if not tastes:
            tastes = ["Eclectic", "Curious", "Creative"]
        
        # Build prompt
        prompt = build_dna_card_prompt(
            username=username,
            archetype=archetype,
            summary=summary,
            tastes=tastes,
            traits=traits_data if traits_data else None
        )
        
        logger.info(f"Generated prompt for DNA card (length: {len(prompt)} chars)")
        
        # Generate image
        negative_prompt = "low quality, blurry, pixelated, boring, generic, corporate, clean UI, dashboard, simple layout, stock photo"
        
        result = image_gen.generate_image(
            prompt=prompt,
            model=model,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            cfg_scale=8.0 if model == "titan" else 7.5
        )
        
        # Store image reference in user profile
        image_id = f"dna-card-{user_id}-{int(datetime.utcnow().timestamp())}"
        
        # Update user with DNA card reference
        db.update(
            table_name=db.users_table,
            key={"userId": user_id},
            update_expression="SET dnaCardImageId = :imageId, dnaCardGeneratedAt = :timestamp",
            expression_values={
                ":imageId": image_id,
                ":timestamp": datetime.utcnow().isoformat()
            }
        )
        
        logger.info(f"DNA card generated successfully: {image_id}")
        
        return {
            "imageId": image_id,
            "imageData": result["image"],  # base64 encoded
            "format": result.get("format", "png"),
            "width": result.get("width", width),
            "height": result.get("height", height),
            "model": result.get("model"),
            "userId": user_id,
            "archetype": archetype
        }
        
    except Exception as e:
        logger.error(f"Error generating DNA card: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    
    # Test with a sample user ID
    test_user_id = "test-user-123"
    
    try:
        result = generate_dna_card(test_user_id)
        print(f"Generated DNA card: {result['imageId']}")
        print(f"Image size: {len(result['imageData'])} bytes (base64)")
    except Exception as e:
        print(f"Error: {e}")
