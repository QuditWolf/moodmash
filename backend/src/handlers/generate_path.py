"""
Generate Growth Path Handler

Generates personalized growth path using Claude.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any

from ..services.bedrock_client import ClaudeService
from ..services.dynamodb_client import DynamoDBClient
from ..utils.validation import validate_user_id, validate_growth_path
from .generate_section1 import load_prompt

logger = logging.getLogger(__name__)


def generate_path(user_id: str) -> Dict[str, Any]:
    """
    Generate growth path recommendations.
    
    Args:
        user_id: User identifier
        
    Returns:
        Growth path dictionary
        
    Raises:
        ValueError: If user not found or no DNA profile
        Exception: If generation fails
    """
    try:
        validate_user_id(user_id)
        
        claude = ClaudeService()
        db = DynamoDBClient()
        
        logger.info(f"Generating growth path for user {user_id}")
        
        # Retrieve user DNA
        user = db.get_user(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
        
        dna_profile = user.get("tasteDNA")
        if not dna_profile:
            raise ValueError(f"User {user_id} has no DNA profile")
        
        # Build DNA context
        dna_context = json.dumps(dna_profile, indent=2)
        
        # Load prompt and inject DNA
        prompt_template = load_prompt("path_prompt.txt")
        prompt = prompt_template.replace("{dna_profile}", dna_context)
        
        # Call Claude to generate path
        response_text = claude.generate_growth_path(prompt, dna_context)
        
        # Parse JSON response
        try:
            growth_path = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {e}")
            raise ValueError("Failed to parse growth path response")
        
        # Validate path structure
        validate_growth_path(growth_path)
        
        # Store path in Users table
        db.update(
            table_name=db.users_table,
            key={"userId": user_id},
            update_expression="SET growthPath = :path, updatedAt = :timestamp",
            expression_values={
                ":path": growth_path,
                ":timestamp": datetime.utcnow().isoformat()
            }
        )
        
        logger.info(f"Growth path generated for user {user_id}")
        
        return growth_path
        
    except Exception as e:
        logger.error(f"Error generating growth path: {e}", exc_info=True)
        raise
