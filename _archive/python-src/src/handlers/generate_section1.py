"""
Generate Section 1 Handler

This module handles generation of Section 1 foundational quiz questions using Claude.
Creates a new session and stores it in DynamoDB.
"""

import json
import logging
import time
import uuid
from typing import Dict, Any, List

from ..services.bedrock_client import get_claude_service
from ..services.dynamodb_client import get_dynamodb_client
from ..utils.logger import get_logger, log_handler_execution, LogContext

logger = get_logger(__name__)


def generate_section1(user_id: str = None) -> Dict[str, Any]:
    """
    Generate Section 1 foundational questions.
    
    Creates 5 foundational questions using Claude and stores session in DynamoDB.
    
    Args:
        user_id: Optional user identifier
        
    Returns:
        Dictionary with sessionId, questions, and expiresAt
        
    Raises:
        Exception: If question generation or session storage fails
    """
    start_time = time.time()
    session_id = str(uuid.uuid4())
    
    try:
        # Generate timestamp
        timestamp = int(time.time())
        expires_at = timestamp + 3600  # 1 hour from now
        
        with LogContext(logger, session_id=session_id, user_id=user_id):
            logger.info(f"Generating Section 1 for session: {session_id}")
            
            # Load prompt for Section 1
            prompt = _get_section1_prompt()
            
            # Call Claude to generate questions
            claude = get_claude_service()
            claude_start = time.time()
            response = claude.invoke(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            claude_duration = time.time() - claude_start
            
            # Log Claude API call
            with LogContext(logger, session_id=session_id, claude_duration_ms=round(claude_duration * 1000, 2)):
                logger.info(f"Claude API call completed in {claude_duration:.3f}s")
            
            # Parse questions from response
            questions = _parse_questions(response)
            
            # Validate we got 5 questions
            if len(questions) != 5:
                raise Exception(f"Expected 5 questions, got {len(questions)}")
            
            # Store session in DynamoDB
            dynamodb = get_dynamodb_client()
            session = {
                'sessionId': session_id,
                'userId': user_id,
                'section1Questions': questions,
                'createdAt': timestamp,
                'expiresAt': expires_at,
                'status': 'section1_complete'
            }
            
            dynamodb.put_item('Sessions', session)
            
            # Log successful completion
            duration = time.time() - start_time
            log_handler_execution(
                logger=logger,
                handler_name='generate_section1',
                duration=duration,
                success=True,
                session_id=session_id,
                question_count=len(questions)
            )
            
            return {
                'sessionId': session_id,
                'questions': questions,
                'expiresAt': expires_at
            }
        
    except Exception as e:
        duration = time.time() - start_time
        
        # Log error with context
        with LogContext(logger, session_id=session_id, user_id=user_id, error_type=type(e).__name__):
            logger.error(f"Failed to generate Section 1: {str(e)}", exc_info=True)
        
        # Log failed execution
        log_handler_execution(
            logger=logger,
            handler_name='generate_section1',
            duration=duration,
            success=False,
            session_id=session_id,
            error=str(e)
        )
        
        raise


def _get_section1_prompt() -> str:
    """
    Get prompt for Section 1 question generation.
    
    Returns:
        Prompt text for Claude
    """
    return """You are a taste profiling expert creating an adaptive quiz to understand someone's unique preferences across content, experiences, and interests.

Generate 5 foundational questions for Section 1 that explore broad taste preferences. These questions should:
- Cover different categories (content, experiences, aesthetics, values, social)
- Be open-ended with multiple choice options
- Allow for multiple selections where appropriate
- Help establish a baseline understanding of the person's taste

Return ONLY a JSON object in this exact format:
{
  "questions": [
    {
      "id": "q1",
      "title": "Question text here?",
      "category": "content|experience|aesthetic|values|social",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"],
      "multiSelect": true|false
    }
  ]
}

Make the questions engaging, thoughtful, and designed to reveal authentic preferences."""


def _parse_questions(claude_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse questions from Claude response.
    
    Args:
        claude_response: Response from Claude API
        
    Returns:
        List of question dictionaries
        
    Raises:
        Exception: If parsing fails
    """
    try:
        # Extract content from response
        content = claude_response.get('content', [])
        if not content:
            raise Exception("No content in Claude response")
        
        # Get text from first content block
        text = content[0].get('text', '')
        if not text:
            raise Exception("No text in Claude response content")
        
        # Find JSON in response (Claude might add explanation text)
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            raise Exception("No JSON found in Claude response")
        
        json_text = text[json_start:json_end]
        
        # Parse JSON
        data = json.loads(json_text)
        
        # Extract questions
        questions = data.get('questions', [])
        if not questions:
            raise Exception("No questions in parsed JSON")
        
        # Validate question structure
        for i, q in enumerate(questions):
            if not all(k in q for k in ['id', 'title', 'category', 'options', 'multiSelect']):
                raise Exception(f"Question {i} missing required fields")
        
        return questions
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from Claude: {str(e)}")
        raise Exception("Failed to parse questions from AI response")
    except Exception as e:
        logger.error(f"Failed to parse questions: {str(e)}")
        raise
