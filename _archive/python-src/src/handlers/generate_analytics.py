"""
Generate Analytics Handler

This module handles generation of behavioral analytics using Claude.
Creates insights and recommendations based on user's taste profile and activity.
"""

import json
import logging
import time
from typing import Dict, Any, List

from ..services.bedrock_client import get_claude_service
from ..services.dynamodb_client import get_dynamodb_client

logger = logging.getLogger(__name__)


def generate_analytics(user_id: str) -> Dict[str, Any]:
    """
    Generate behavioral analytics for user.
    
    Analyzes user's DNA profile and growth path to generate insights.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary with analytics data
        
    Raises:
        Exception: If user not found or analytics generation fails
    """
    try:
        logger.info(f"Generating analytics for user: {user_id}")
        
        # Retrieve user profile
        dynamodb = get_dynamodb_client()
        user = dynamodb.get_item('Users', {'userId': user_id})
        
        if not user:
            raise Exception("User not found")
        
        # Get DNA and growth path
        taste_dna = user.get('tasteDNA', {})
        growth_path = user.get('growthPath', {})
        
        # Build analytics context
        context = _build_analytics_context(taste_dna, growth_path)
        
        # Get analytics generation prompt
        prompt = _get_analytics_prompt(context)
        
        # Call Claude to generate analytics
        claude = get_claude_service()
        response = claude.invoke(
            prompt=prompt,
            temperature=0.6,
            max_tokens=2000
        )
        
        # Parse analytics from response
        analytics = _parse_analytics(response)
        
        # Validate analytics structure
        _validate_analytics(analytics)
        
        # Add timestamp
        timestamp = int(time.time())
        analytics['generatedAt'] = timestamp
        
        # Store analytics in Users table
        dynamodb.update_item(
            'Users',
            {'userId': user_id},
            {
                'analytics': analytics,
                'analyticsGeneratedAt': timestamp,
                'updatedAt': timestamp
            }
        )
        
        logger.info(f"Analytics generated successfully for user: {user_id}")
        
        return {'analytics': analytics}
        
    except Exception as e:
        logger.error(f"Failed to generate analytics: {str(e)}", exc_info=True)
        raise


def _build_analytics_context(
    taste_dna: Dict[str, Any],
    growth_path: Dict[str, Any]
) -> str:
    """
    Build context string for analytics generation.
    
    Args:
        taste_dna: User's taste DNA profile
        growth_path: User's growth path
        
    Returns:
        Context string for Claude
    """
    context_parts = []
    
    # DNA summary
    context_parts.append("=== Taste DNA ===")
    context_parts.append(f"Archetype: {taste_dna.get('archetype', 'Unknown')}")
    context_parts.append("\nTraits:")
    for trait in taste_dna.get('traits', []):
        context_parts.append(f"- {trait.get('name')}: {trait.get('score')}/10")
    
    # Growth path summary
    if growth_path:
        context_parts.append("\n=== Growth Path ===")
        context_parts.append(f"Absorb items: {len(growth_path.get('absorb', []))}")
        context_parts.append(f"Create items: {len(growth_path.get('create', []))}")
        context_parts.append(f"Reflect items: {len(growth_path.get('reflect', []))}")
    
    return "\n".join(context_parts)


def _get_analytics_prompt(context: str) -> str:
    """
    Get prompt for analytics generation.
    
    Args:
        context: Context from user profile
        
    Returns:
        Prompt text for Claude
    """
    return f"""You are a behavioral analyst creating insights about someone's taste development and content consumption patterns.

Here is their profile:

{context}

Generate analytics that include:
1. Passive vs Intentional Ratio: Estimate how much they consume passively vs intentionally (0-1 scale)
2. Goal Alignment: How well their current path aligns with their stated preferences (0-10 scale)
3. Content Balance: Distribution across different categories with trends
4. Insights: 3-5 key observations (strengths, opportunities, patterns)
5. Recommendations: 3-5 actionable suggestions for growth

Return ONLY a JSON object in this exact format:
{{
  "passiveVsIntentionalRatio": 0.65,
  "goalAlignment": 7.5,
  "contentBalance": [
    {{
      "category": "Category name",
      "percentage": 35.0,
      "trend": "increasing|stable|decreasing"
    }}
  ],
  "insights": [
    {{
      "type": "strength|opportunity|pattern",
      "title": "Insight title",
      "description": "Detailed insight description"
    }}
  ],
  "recommendations": [
    "Specific actionable recommendation 1",
    "Specific actionable recommendation 2"
  ]
}}

Make insights meaningful and recommendations actionable."""


def _parse_analytics(claude_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse analytics from Claude response.
    
    Args:
        claude_response: Response from Claude API
        
    Returns:
        Analytics dictionary
        
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
        analytics = json.loads(json_text)
        
        return analytics
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from Claude: {str(e)}")
        raise Exception("Failed to parse analytics from AI response")
    except Exception as e:
        logger.error(f"Failed to parse analytics: {str(e)}")
        raise


def _validate_analytics(analytics: Dict[str, Any]) -> None:
    """
    Validate analytics structure.
    
    Args:
        analytics: Analytics to validate
        
    Raises:
        ValueError: If validation fails
    """
    # Check required fields
    required_fields = [
        'passiveVsIntentionalRatio',
        'goalAlignment',
        'contentBalance',
        'insights',
        'recommendations'
    ]
    
    for field in required_fields:
        if field not in analytics:
            raise ValueError(f"Analytics missing required field: {field}")
    
    # Validate ratio
    ratio = analytics['passiveVsIntentionalRatio']
    if not (0 <= ratio <= 1):
        raise ValueError(f"Ratio must be 0-1, got {ratio}")
    
    # Validate goal alignment
    alignment = analytics['goalAlignment']
    if not (0 <= alignment <= 10):
        raise ValueError(f"Goal alignment must be 0-10, got {alignment}")
    
    # Validate content balance
    content_balance = analytics['contentBalance']
    if not isinstance(content_balance, list):
        raise ValueError("Content balance must be a list")
    
    for item in content_balance:
        if not all(k in item for k in ['category', 'percentage', 'trend']):
            raise ValueError("Content balance item missing required fields")
        
        if item['trend'] not in ['increasing', 'stable', 'decreasing']:
            raise ValueError(f"Invalid trend: {item['trend']}")
    
    # Validate insights
    insights = analytics['insights']
    if not isinstance(insights, list):
        raise ValueError("Insights must be a list")
    
    for insight in insights:
        if not all(k in insight for k in ['type', 'title', 'description']):
            raise ValueError("Insight missing required fields")
        
        if insight['type'] not in ['strength', 'opportunity', 'pattern']:
            raise ValueError(f"Invalid insight type: {insight['type']}")
    
    # Validate recommendations
    recommendations = analytics['recommendations']
    if not isinstance(recommendations, list):
        raise ValueError("Recommendations must be a list")
