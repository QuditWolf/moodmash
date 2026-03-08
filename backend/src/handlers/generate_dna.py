"""
Generate DNA Handler

Generates taste DNA profile using Claude.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

from ..services.bedrock_client import ClaudeService
from ..services.dynamodb_client import DynamoDBClient
from ..utils.validation import validate_user_id, validate_taste_dna
from .generate_section1 import load_prompt

logger = logging.getLogger(__name__)


def generate_dna(
    user_id: str,
    section1_answers: List[Dict[str, Any]],
    section2_answers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate taste DNA profile.
    
    Args:
        user_id: User identifier
        section1_answers: Section 1 answers
        section2_answers: Section 2 answers
        
    Returns:
        Taste DNA profile dictionary
        
    Raises:
        ValueError: If inputs invalid or user not found
        Exception: If generation fails
    """
    try:
        # Validate inputs
        validate_user_id(user_id)
        
        # Initialize services
        claude = ClaudeService()
        db = DynamoDBClient()
        
        logger.info(f"Generating DNA for user {user_id}")
        
        # Build quiz summary
        summary_parts = ["Section 1 Responses:"]
        for answer in section1_answers:
            category = answer.get("category", "unknown")
            selected = answer.get("selectedOptions", [])
            summary_parts.append(f"- {category}: {', '.join(selected)}")
        
        summary_parts.append("\nSection 2 Responses:")
        for answer in section2_answers:
            category = answer.get("category", "unknown")
            selected = answer.get("selectedOptions", [])
            summary_parts.append(f"- {category}: {', '.join(selected)}")
        
        quiz_summary = "\n".join(summary_parts)
        
        # Load prompt and inject summary
        prompt_template = load_prompt("dna_prompt.txt")
        prompt = prompt_template.replace("{quiz_summary}", quiz_summary)
        
        # Call Claude to generate DNA
        response_text = claude.generate_taste_dna(prompt, quiz_summary)
        
        # Parse JSON response
        try:
            dna_profile = json.loads(response_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError("Failed to parse DNA generation response")
        
        # Validate DNA structure
        validate_taste_dna(dna_profile)
        
        # Store DNA in Users table
        user = db.get_user(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
        
        db.update(
            table_name=db.users_table,
            key={"userId": user_id},
            update_expression=(
                "SET tasteDNA = :dna, "
                "updatedAt = :timestamp"
            ),
            expression_values={
                ":dna": dna_profile,
                ":timestamp": datetime.utcnow().isoformat()
            }
        )
        
        logger.info(f"DNA generated and stored for user {user_id}")
        
        return dna_profile
        
    except Exception as e:
        logger.error(f"Error generating DNA: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    test_s1 = [
        {"questionId": "q1", "selectedOptions": ["Visual art"], "category": "content"},
        {"questionId": "q2", "selectedOptions": ["Exploring"], "category": "discovery"},
        {"questionId": "q3", "selectedOptions": ["Calm"], "category": "mood"},
        {"questionId": "q4", "selectedOptions": ["Observe"], "category": "engagement"},
        {"questionId": "q5", "selectedOptions": ["Aesthetic"], "category": "attraction"}
    ]
    test_s2 = [
        {"questionId": "q6", "selectedOptions": ["Minimalist"], "category": "visual"},
        {"questionId": "q7", "selectedOptions": ["Personal"], "category": "narrative"},
        {"questionId": "q8", "selectedOptions": ["Learning"], "category": "activity"},
        {"questionId": "q9", "selectedOptions": ["Contemporary"], "category": "cultural"},
        {"questionId": "q10", "selectedOptions": ["Focused"], "category": "identity"}
    ]
    
    # result = generate_dna("test-user", test_s1, test_s2)
    # print(json.dumps(result, indent=2))
