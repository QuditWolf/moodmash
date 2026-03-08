"""
Generate Section 2 Handler

Generates adaptive quiz questions based on Section 1 answers.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any

from ..services.bedrock_client import ClaudeService
from ..services.dynamodb_client import DynamoDBClient
from ..utils.validation import validate_session_id, validate_section1_answers
from .generate_section1 import load_prompt

logger = logging.getLogger(__name__)


def generate_section2(
    session_id: str,
    section1_answers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate Section 2 adaptive questions.
    
    Args:
        session_id: Session identifier
        section1_answers: List of Section 1 answers
        
    Returns:
        Dictionary with questions
        
    Raises:
        ValueError: If session not found or answers invalid
        Exception: If generation fails
    """
    try:
        # Validate inputs
        validate_session_id(session_id)
        validate_section1_answers(section1_answers)
        
        # Initialize services
        claude = ClaudeService()
        db = DynamoDBClient()
        
        logger.info(f"Generating Section 2 for session {session_id}")
        
        # Retrieve session
        session = db.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Build context from Section 1 answers
        context_parts = []
        for answer in section1_answers:
            question_id = answer.get("questionId")
            selected = answer.get("selectedOptions", [])
            category = answer.get("category", "unknown")
            
            if selected:
                context_parts.append(
                    f"- {category}: {', '.join(selected)}"
                )
        
        section1_context = "\n".join(context_parts)
        
        # Load prompt and inject context
        prompt_template = load_prompt("section2_prompt.txt")
        prompt = prompt_template.replace("{section1_context}", section1_context)
        
        # Call Claude to generate adaptive questions
        response_text = claude.generate_questions(
            prompt,
            num_questions=5,
            context=section1_context
        )
        
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
        
        # Update session with Section 1 answers and Section 2 questions
        db.update(
            table_name=db.sessions_table,
            key={"sessionId": session_id},
            update_expression=(
                "SET #status = :status, "
                "section1Answers = :s1answers, "
                "section2Questions = :s2questions, "
                "updatedAt = :timestamp"
            ),
            expression_names={
                "#status": "status"
            },
            expression_values={
                ":status": "section2_complete",
                ":s1answers": section1_answers,
                ":s2questions": questions,
                ":timestamp": datetime.utcnow().isoformat()
            }
        )
        
        logger.info(f"Section 2 generated successfully: {len(questions)} questions")
        
        return {
            "questions": questions
        }
        
    except Exception as e:
        logger.error(f"Error generating Section 2: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # For testing
    logging.basicConfig(level=logging.INFO)
    
    # Example usage
    test_answers = [
        {
            "questionId": "q1",
            "selectedOptions": ["Visual art", "Photography"],
            "category": "content_preference"
        },
        {
            "questionId": "q2",
            "selectedOptions": ["By exploring"],
            "category": "discovery_style"
        },
        {
            "questionId": "q3",
            "selectedOptions": ["Calm", "Reflective"],
            "category": "mood_preference"
        },
        {
            "questionId": "q4",
            "selectedOptions": ["Observe"],
            "category": "engagement_style"
        },
        {
            "questionId": "q5",
            "selectedOptions": ["Aesthetic appeal"],
            "category": "attraction_factors"
        }
    ]
    
    # Note: Need valid session_id from generate_section1
    # result = generate_section2("test-session-id", test_answers)
    # print(json.dumps(result, indent=2))
