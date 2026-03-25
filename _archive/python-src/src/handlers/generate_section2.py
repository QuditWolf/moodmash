"""
Generate Section 2 Handler

This module handles generation of adaptive Section 2 questions based on Section 1 answers.
"""

import json
import logging
import time
from typing import Dict, Any, List

from ..services.bedrock_client import get_claude_service
from ..services.dynamodb_client import get_dynamodb_client

logger = logging.getLogger(__name__)


def generate_section2(session_id: str, section1_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate adaptive Section 2 questions based on Section 1 answers.
    
    Args:
        session_id: Session identifier
        section1_answers: List of answers from Section 1
        
    Returns:
        Dictionary with Section 2 questions
        
    Raises:
        Exception: If session not found, expired, or generation fails
    """
    try:
        logger.info(f"Generating Section 2 for session: {session_id}")
        
        # Retrieve session from DynamoDB
        dynamodb = get_dynamodb_client()
        session = dynamodb.get_item('Sessions', {'sessionId': session_id})
        
        if not session:
            raise Exception("Session not found")
        
        # Check if session expired
        current_time = int(time.time())
        expires_at = session.get('expiresAt', 0)
        if current_time > expires_at:
            raise Exception("Session expired")
        
        # Get Section 1 questions for context
        section1_questions = session.get('section1Questions', [])
        
        # Build context from Section 1 answers
        context = _build_answer_context(section1_questions, section1_answers)
        
        # Get prompt for Section 2 with context
        prompt = _get_section2_prompt(context)
        
        # Call Claude to generate adaptive questions
        claude = get_claude_service()
        response = claude.invoke(
            prompt=prompt,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse questions from response
        questions = _parse_questions(response)
        
        # Validate we got 5 questions
        if len(questions) != 5:
            raise Exception(f"Expected 5 questions, got {len(questions)}")
        
        # Update session with Section 1 answers and Section 2 questions
        dynamodb.update_item(
            'Sessions',
            {'sessionId': session_id},
            {
                'section1Answers': section1_answers,
                'section2Questions': questions,
                'status': 'section2_complete'
            }
        )
        
        logger.info(f"Section 2 generated successfully for session: {session_id}")
        
        return {'questions': questions}
        
    except Exception as e:
        logger.error(f"Failed to generate Section 2: {str(e)}", exc_info=True)
        raise


def _build_answer_context(
    questions: List[Dict[str, Any]],
    answers: List[Dict[str, Any]]
) -> str:
    """
    Build context string from Section 1 questions and answers.
    
    Args:
        questions: Section 1 questions
        answers: Section 1 answers
        
    Returns:
        Context string for Claude
    """
    context_parts = []
    
    # Create answer lookup by question ID
    answer_map = {a['questionId']: a['selectedOptions'] for a in answers}
    
    for q in questions:
        q_id = q['id']
        q_title = q['title']
        selected = answer_map.get(q_id, [])
        
        if selected:
            context_parts.append(f"Q: {q_title}")
            context_parts.append(f"A: {', '.join(selected)}")
            context_parts.append("")
    
    return "\n".join(context_parts)


def _get_section2_prompt(context: str) -> str:
    """
    Get prompt for Section 2 question generation with context.
    
    Args:
        context: Context from Section 1 answers
        
    Returns:
        Prompt text for Claude
    """
    return f"""You are a taste profiling expert creating adaptive quiz questions based on someone's initial responses.

Here are their Section 1 answers:

{context}

Based on these answers, generate 5 personalized Section 2 questions that:
- Dive deeper into the preferences they've shown
- Explore nuances and specific aspects of their taste
- Help distinguish their unique profile from others
- Build on patterns you notice in their Section 1 responses
- Remain engaging and thought-provoking

Return ONLY a JSON object in this exact format:
{{
  "questions": [
    {{
      "id": "q6",
      "title": "Question text here?",
      "category": "content|experience|aesthetic|values|social",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"],
      "multiSelect": true|false
    }}
  ]
}}

Make the questions feel personalized to their Section 1 responses."""


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
        
        # Find JSON in response
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
