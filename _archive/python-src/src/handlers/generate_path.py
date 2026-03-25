"""
Generate Growth Path Handler

This module handles generation of personalized growth paths using Claude.
Creates Absorb/Create/Reflect recommendations based on taste DNA.
"""

import json
import logging
import time
from typing import Dict, Any, List

from ..services.bedrock_client import get_claude_service
from ..services.dynamodb_client import get_dynamodb_client

logger = logging.getLogger(__name__)


def generate_path(user_id: str) -> Dict[str, Any]:
    """
    Generate personalized growth path for user.
    
    Retrieves user's DNA profile and generates Absorb/Create/Reflect recommendations.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary with growth path
        
    Raises:
        Exception: If user not found or path generation fails
    """
    try:
        logger.info(f"Generating growth path for user: {user_id}")
        
        # Retrieve user profile
        dynamodb = get_dynamodb_client()
        user = dynamodb.get_item('Users', {'userId': user_id})
        
        if not user:
            raise Exception("User not found")
        
        # Get DNA profile
        taste_dna = user.get('tasteDNA')
        if not taste_dna:
            raise Exception("User DNA profile not found")
        
        # Build context from DNA
        context = _build_dna_context(taste_dna)
        
        # Get path generation prompt
        prompt = _get_path_prompt(context)
        
        # Call Claude to generate growth path
        claude = get_claude_service()
        response = claude.invoke(
            prompt=prompt,
            temperature=0.7,
            max_tokens=2500
        )
        
        # Parse growth path from response
        growth_path = _parse_growth_path(response)
        
        # Validate path structure
        _validate_growth_path(growth_path)
        
        # Add timestamp
        timestamp = int(time.time())
        growth_path['generatedAt'] = timestamp
        
        # Store path in Users table
        dynamodb.update_item(
            'Users',
            {'userId': user_id},
            {
                'growthPath': growth_path,
                'pathGeneratedAt': timestamp,
                'updatedAt': timestamp
            }
        )
        
        logger.info(f"Growth path generated successfully for user: {user_id}")
        
        return {'path': growth_path}
        
    except Exception as e:
        logger.error(f"Failed to generate growth path: {str(e)}", exc_info=True)
        raise


def _build_dna_context(taste_dna: Dict[str, Any]) -> str:
    """
    Build context string from DNA profile.
    
    Args:
        taste_dna: User's taste DNA profile
        
    Returns:
        Context string for Claude
    """
    context_parts = []
    
    # Archetype
    context_parts.append(f"Archetype: {taste_dna.get('archetype', 'Unknown')}")
    context_parts.append("")
    
    # Traits
    context_parts.append("Key Traits:")
    for trait in taste_dna.get('traits', []):
        name = trait.get('name', '')
        score = trait.get('score', 0)
        context_parts.append(f"- {name}: {score}/10")
    context_parts.append("")
    
    # Categories
    context_parts.append("Category Preferences:")
    for category in taste_dna.get('categories', []):
        cat_name = category.get('category', '')
        intensity = category.get('intensity', 0)
        prefs = category.get('preferences', [])
        context_parts.append(f"- {cat_name} (intensity: {intensity}/10)")
        for pref in prefs[:3]:  # Top 3 preferences
            context_parts.append(f"  • {pref}")
    
    return "\n".join(context_parts)


def _get_path_prompt(context: str) -> str:
    """
    Get prompt for growth path generation.
    
    Args:
        context: Context from DNA profile
        
    Returns:
        Prompt text for Claude
    """
    return f"""You are a personalized growth advisor creating a tailored development path based on someone's taste profile.

Here is their Taste DNA:

{context}

Create a personalized growth path with three categories:

1. ABSORB: Content to consume (books, articles, videos, podcasts, courses)
2. CREATE: Projects or activities to make/do
3. REFLECT: Practices for self-awareness and integration

Each category should have 3-5 specific, actionable recommendations that:
- Align with their taste profile and preferences
- Challenge them appropriately
- Build on their strengths
- Address growth opportunities

Return ONLY a JSON object in this exact format:
{{
  "absorb": [
    {{
      "id": "abs1",
      "title": "Recommendation title",
      "description": "Detailed description of what and why",
      "category": "books|videos|podcasts|courses|articles",
      "estimatedTime": "2 hours|1 week|etc",
      "difficulty": "beginner|intermediate|advanced"
    }}
  ],
  "create": [
    {{
      "id": "cre1",
      "title": "Project title",
      "description": "What to create and how it helps",
      "category": "writing|art|music|code|design|etc",
      "estimatedTime": "3 hours|2 weeks|etc",
      "difficulty": "beginner|intermediate|advanced"
    }}
  ],
  "reflect": [
    {{
      "id": "ref1",
      "title": "Practice title",
      "description": "Reflection practice and its benefits",
      "category": "journaling|meditation|discussion|analysis",
      "estimatedTime": "15 minutes|daily|weekly",
      "difficulty": "beginner|intermediate|advanced"
    }}
  ]
}}

Make recommendations specific, meaningful, and personalized to their profile."""


def _parse_growth_path(claude_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse growth path from Claude response.
    
    Args:
        claude_response: Response from Claude API
        
    Returns:
        Growth path dictionary
        
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
        growth_path = json.loads(json_text)
        
        return growth_path
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from Claude: {str(e)}")
        raise Exception("Failed to parse growth path from AI response")
    except Exception as e:
        logger.error(f"Failed to parse growth path: {str(e)}")
        raise


def _validate_growth_path(growth_path: Dict[str, Any]) -> None:
    """
    Validate growth path structure.
    
    Args:
        growth_path: Growth path to validate
        
    Raises:
        ValueError: If validation fails
    """
    # Check required categories
    required_categories = ['absorb', 'create', 'reflect']
    for category in required_categories:
        if category not in growth_path:
            raise ValueError(f"Growth path missing category: {category}")
        
        items = growth_path[category]
        if not isinstance(items, list):
            raise ValueError(f"Category {category} must be a list")
        
        if not (3 <= len(items) <= 5):
            raise ValueError(f"Category {category} must have 3-5 items, got {len(items)}")
        
        # Validate each item
        for item in items:
            required_fields = ['id', 'title', 'description', 'category', 
                             'estimatedTime', 'difficulty']
            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Path item missing field: {field}")
            
            # Validate difficulty
            if item['difficulty'] not in ['beginner', 'intermediate', 'advanced']:
                raise ValueError(f"Invalid difficulty: {item['difficulty']}")
