"""
Generate Section 1 Handler

Generates foundational quiz questions using Claude.
"""

import json
import uuid
import os
import logging
from datetime import datetime
from typing import Dict, List, Any

from ..services.bedrock_client import ClaudeService
from ..services.dynamodb_client import DynamoDBClient

logger = logging.getLogger(__name__)


def load_prompt(prompt_file: str) -> str:
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


def generate_section1() -> Dict[str, Any]:
    """
    Generate Section 1 quiz questions.
    
    Returns:
        Dictionary with sessionId and questions
        
    Raises:
        Exception: If generation fails
    """
    try:
        # Initialize services
        claude = ClaudeService()
        db = DynamoDBClient()
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        logger.info(f"Generating Section 1 for session {session_id}")
        
        # Load prompt
        prompt = load_prompt("section1_prompt.txt")
        
        # Call Claude to generate questions
        response_text = claude.generate_questions(prompt, num_questions=5)
        
        # Parse JSON response
        try:
            response_data = json.loads(response_text)
            questions = response_data.get("questions", [])
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {e}")
            logger.error(f"Response text: {response_text}")
            raise ValueError("Failed to parse question generation response")
        
        # Validate questions
        if len(questions) != 5:
            logger.warning(f"Expected 5 questions, got {len(questions)}")
        
        # Store session in DynamoDB
        session_data = {
            "sessionId": session_id,
            "status": "section1_complete",
            "section1Questions": questions,
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        }
        
        db.put_session(session_data)
        
        logger.info(f"Section 1 generated successfully: {len(questions)} questions")
        
        return {
            "sessionId": session_id,
            "questions": questions
        }
        
    except Exception as e:
        logger.error(f"Error generating Section 1: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    result = generate_section1()
    print(json.dumps(result, indent=2))
