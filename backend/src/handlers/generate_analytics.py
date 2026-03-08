"""
Generate Analytics Handler

Generates behavioral analytics using Claude.
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any

from ..services.bedrock_client import ClaudeService
from ..services.dynamodb_client import DynamoDBClient
from ..utils.validation import validate_user_id
from .generate_section1 import load_prompt

logger = logging.getLogger(__name__)


def generate_analytics(user_id: str) -> Dict[str, Any]:
    """
    Generate behavioral analytics.
    
    Args:
        user_id: User identifier
        
    Returns:
        Analytics dictionary
        
    Raises:
        ValueError: If user not found
        Exception: If generation fails
    """
    try:
        validate_user_id(user_id)
        
        claude = ClaudeService()
        db = DynamoDBClient()
        
        logger.info(f"Generating analytics for user {user_id}")
        
        # Retrieve user data
        user = db.get_user(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
        
        # Build user data context
        user_data = {
            "tasteDNA": user.get("tasteDNA", {}),
            "growthPath": user.get("growthPath", {}),
            "answerMetadata": user.get("answerMetadata", {})
        }
        
        user_context = json.dumps(user_data, indent=2)
        
        # Load prompt and inject user data
        prompt_template = load_prompt("analytics_prompt.txt")
        prompt = prompt_template.replace("{user_data}", user_context)
        
        # Call Claude to generate analytics
        response_text = claude.generate_analytics(prompt, user_context)
        
        # Parse JSON response
        try:
            analytics = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {e}")
            raise ValueError("Failed to parse analytics response")
        
        # Validate analytics structure
        if "insights" not in analytics:
            raise ValueError("Analytics missing 'insights' field")
        
        # Store analytics in Users table
        db.update(
            table_name=db.users_table,
            key={"userId": user_id},
            update_expression="SET analytics = :analytics, updatedAt = :timestamp",
            expression_values={
                ":analytics": analytics,
                ":timestamp": datetime.utcnow().isoformat()
            }
        )
        
        logger.info(f"Analytics generated for user {user_id}")
        
        return analytics
        
    except Exception as e:
        logger.error(f"Error generating analytics: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    
    # result = generate_analytics("test-user")
    # print(json.dumps(result, indent=2))
