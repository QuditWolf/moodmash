"""
Generate DNA Handler

This module handles generation of taste DNA profiles using Claude.
Creates archetype, traits, and category profiles.
"""

import json
import logging
import time
from typing import Dict, Any, List

from ..services.bedrock_client import get_claude_service
from ..services.dynamodb_client import get_dynamodb_client

logger = logging.getLogger(__name__)


def generate_dna(user_id: str, all_answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate taste DNA profile from quiz answers.
    
    Uses Claude to analyze answers and create personalized archetype with traits.
    
    Args:
        user_id: User identifier
        all_answers: Dictionary with section1 and section2 answers
        
    Returns:
        Dictionary with taste DNA profile
        
    Raises:
        Exception: If DNA generation fails
    """
    try:
        logger.info(f"Generating DNA profile for user: {user_id}")
        
        # Build answer summary for Claude
        answer_summary = _summarize_answers(all_answers)
        
        # Get DNA generation prompt
        prompt = _get_dna_prompt(answer_summary)
        
        # Call Claude to generate DNA profile
        claude = get_claude_service()
        response = claude.invoke(
            prompt=prompt,
            temperature=0.8,
            max_tokens=1500
        )
        
        # Parse DNA profile from response
        dna_profile = _parse_dna_profile(response)
        
        # Validate DNA structure
        _validate_dna_profile(dna_profile)
        
        # Store DNA profile in Users table
        dynamodb = get_dynamodb_client()
        timestamp = int(time.time())
        
        dynamodb.update_item(
            'Users',
            {'userId': user_id},
            {
                'tasteDNA': dna_profile,
                'dnaGeneratedAt': timestamp,
                'updatedAt': timestamp
            }
        )
        
        logger.info(f"DNA profile generated: {dna_profile['archetype']}")
        
        return dna_profile
        
    except Exception as e:
        logger.error(f"Failed to generate DNA: {str(e)}", exc_info=True)
        raise


def _summarize_answers(all_answers: Dict[str, Any]) -> str:
    """
    Summarize quiz answers for DNA generation.
    
    Args:
        all_answers: Dictionary with section1 and section2 answers
        
    Returns:
        Summary string
    """
    summary_parts = []
    
    # Section 1
    summary_parts.append("=== Section 1 Responses ===")
    for i, answer in enumerate(all_answers.get('section1', []), 1):
        options = answer.get('selectedOptions', [])
        summary_parts.append(f"{i}. {', '.join(options)}")
    
    # Section 2
    summary_parts.append("\n=== Section 2 Responses ===")
    for i, answer in enumerate(all_answers.get('section2', []), 1):
        options = answer.get('selectedOptions', [])
        summary_parts.append(f"{i}. {', '.join(options)}")
    
    return "\n".join(summary_parts)


def _get_dna_prompt(answer_summary: str) -> str:
    """
    Get prompt for DNA generation.
    
    Args:
        answer_summary: Summary of quiz answers
        
    Returns:
        Prompt text for Claude
    """
    return f"""You are a taste profiling expert analyzing someone's quiz responses to create their unique Taste DNA profile.

Here are their quiz responses:

{answer_summary}

Based on these responses, create a comprehensive Taste DNA profile that includes:
1. A memorable archetype name (e.g., "The Curious Explorer", "The Minimalist Curator")
2. 5-7 personality traits with scores (0-10) and descriptions
3. Category profiles showing their preferences across different content types
4. An overall description of their taste personality

Return ONLY a JSON object in this exact format:
{{
  "archetype": "The [Archetype Name]",
  "traits": [
    {{
      "name": "Trait name",
      "score": 7.5,
      "description": "Brief description of this trait"
    }}
  ],
  "categories": [
    {{
      "category": "Category name",
      "preferences": ["Specific preference 1", "Specific preference 2"],
      "intensity": 8.0
    }}
  ],
  "description": "A paragraph describing their overall taste personality and what makes them unique"
}}

Make it insightful, accurate, and personally meaningful."""


def _parse_dna_profile(claude_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse DNA profile from Claude response.
    
    Args:
        claude_response: Response from Claude API
        
    Returns:
        DNA profile dictionary
        
    Raises:
        Exception: If parsing fails
    """
    try:
        # Extract content from response
        content = claude_response.get('content', [])
        if not content:
            raise Exception("No content in Claude response")
        
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
        dna_profile = json.loads(json_text)
        
        return dna_profile
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from Claude: {str(e)}")
        raise Exception("Failed to parse DNA profile from AI response")
    except Exception as e:
        logger.error(f"Failed to parse DNA profile: {str(e)}")
        raise


def _validate_dna_profile(dna_profile: Dict[str, Any]) -> None:
    """
    Validate DNA profile structure.
    
    Args:
        dna_profile: DNA profile to validate
        
    Raises:
        ValueError: If validation fails
    """
    # Check required fields
    required_fields = ['archetype', 'traits', 'categories', 'description']
    for field in required_fields:
        if field not in dna_profile:
            raise ValueError(f"DNA profile missing required field: {field}")
    
    # Validate traits
    traits = dna_profile['traits']
    if not isinstance(traits, list) or len(traits) == 0:
        raise ValueError("DNA profile must have at least one trait")
    
    for trait in traits:
        if not all(k in trait for k in ['name', 'score', 'description']):
            raise ValueError("Trait missing required fields")
        
        score = trait['score']
        if not (0 <= score <= 10):
            raise ValueError(f"Trait score must be 0-10, got {score}")
    
    # Validate categories
    categories = dna_profile['categories']
    if not isinstance(categories, list) or len(categories) == 0:
        raise ValueError("DNA profile must have at least one category")
    
    for category in categories:
        if not all(k in category for k in ['category', 'preferences', 'intensity']):
            raise ValueError("Category missing required fields")
