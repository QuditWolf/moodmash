"""
Validation Utilities

Provides input validation for quiz answers, IDs, and data structures.
"""

import re
import uuid
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def validate_uuid(value: str, field_name: str = "id") -> bool:
    """
    Validate UUID format.
    
    Args:
        value: String to validate as UUID
        field_name: Name of field for error messages
        
    Returns:
        True if valid UUID
        
    Raises:
        ValueError: If not a valid UUID
        
    Example:
        >>> validate_uuid("550e8400-e29b-41d4-a716-446655440000")
        True
    """
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError) as e:
        raise ValueError(f"Invalid {field_name}: must be a valid UUID, got '{value}'")


def validate_quiz_answers(
    answers: List[Dict[str, Any]],
    expected_count: int = 5,
    section_name: str = "section"
) -> bool:
    """
    Validate quiz answer structure and content.
    
    Args:
        answers: List of answer dictionaries
        expected_count: Expected number of answers (default: 5)
        section_name: Name of section for error messages
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If answers are invalid with descriptive error
        
    Example:
        >>> answers = [
        ...     {"questionId": "q1", "selectedOptions": ["opt1"], "category": "test"}
        ... ]
        >>> validate_quiz_answers(answers, expected_count=1)
        True
    """
    # Check answer count
    if len(answers) != expected_count:
        raise ValueError(
            f"{section_name} must have exactly {expected_count} answers, "
            f"got {len(answers)}"
        )
    
    # Validate each answer
    for i, answer in enumerate(answers):
        # Check required fields
        if "questionId" not in answer:
            raise ValueError(
                f"{section_name} answer {i+1} missing required field 'questionId'"
            )
        
        if "selectedOptions" not in answer:
            raise ValueError(
                f"{section_name} answer {i+1} missing required field 'selectedOptions'"
            )
        
        # Validate selectedOptions
        selected = answer["selectedOptions"]
        if not isinstance(selected, list):
            raise ValueError(
                f"{section_name} answer {i+1} 'selectedOptions' must be a list"
            )
        
        if len(selected) == 0:
            raise ValueError(
                f"{section_name} answer {i+1} must have at least one selected option"
            )
        
        # Validate option strings
        for j, option in enumerate(selected):
            if not isinstance(option, str):
                raise ValueError(
                    f"{section_name} answer {i+1} option {j+1} must be a string"
                )
            
            if len(option) > 500:
                raise ValueError(
                    f"{section_name} answer {i+1} option {j+1} exceeds 500 characters"
                )
            
            if len(option.strip()) == 0:
                raise ValueError(
                    f"{section_name} answer {i+1} option {j+1} cannot be empty"
                )
    
    return True


def validate_section1_answers(answers: List[Dict[str, Any]]) -> bool:
    """
    Validate Section 1 answers (5 foundational questions).
    
    Args:
        answers: List of Section 1 answers
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If invalid
    """
    return validate_quiz_answers(answers, expected_count=5, section_name="Section 1")


def validate_section2_answers(answers: List[Dict[str, Any]]) -> bool:
    """
    Validate Section 2 answers (5 adaptive questions).
    
    Args:
        answers: List of Section 2 answers
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If invalid
    """
    return validate_quiz_answers(answers, expected_count=5, section_name="Section 2")


def validate_answer_structure(answer: Dict[str, Any]) -> bool:
    """
    Validate individual answer structure.
    
    Args:
        answer: Single answer dictionary
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If invalid
    """
    required_fields = ["questionId", "selectedOptions"]
    
    for field in required_fields:
        if field not in answer:
            raise ValueError(f"Answer missing required field '{field}'")
    
    if not isinstance(answer["selectedOptions"], list):
        raise ValueError("selectedOptions must be a list")
    
    if len(answer["selectedOptions"]) == 0:
        raise ValueError("selectedOptions cannot be empty")
    
    return True


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format.
    
    Args:
        user_id: User identifier
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If invalid
    """
    if not user_id or not isinstance(user_id, str):
        raise ValueError("userId must be a non-empty string")
    
    if len(user_id) > 128:
        raise ValueError("userId cannot exceed 128 characters")
    
    # Allow alphanumeric, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        raise ValueError(
            "userId can only contain alphanumeric characters, hyphens, and underscores"
        )
    
    return True


def validate_session_id(session_id: str) -> bool:
    """
    Validate session ID format (must be UUID).
    
    Args:
        session_id: Session identifier
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If invalid
    """
    return validate_uuid(session_id, "sessionId")


def validate_taste_dna(dna: Dict[str, Any]) -> bool:
    """
    Validate taste DNA structure.
    
    Args:
        dna: Taste DNA dictionary
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If invalid
    """
    required_fields = ["archetype", "description", "traits", "categories"]
    
    for field in required_fields:
        if field not in dna:
            raise ValueError(f"Taste DNA missing required field '{field}'")
    
    # Validate traits
    if not isinstance(dna["traits"], list):
        raise ValueError("Taste DNA 'traits' must be a list")
    
    for trait in dna["traits"]:
        if "name" not in trait or "score" not in trait:
            raise ValueError("Each trait must have 'name' and 'score'")
        
        score = trait["score"]
        if not isinstance(score, (int, float)) or score < 0 or score > 10:
            raise ValueError(f"Trait score must be between 0 and 10, got {score}")
    
    # Validate categories
    if not isinstance(dna["categories"], dict):
        raise ValueError("Taste DNA 'categories' must be a dictionary")
    
    return True


def validate_growth_path(path: Dict[str, Any]) -> bool:
    """
    Validate growth path structure.
    
    Args:
        path: Growth path dictionary
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If invalid
    """
    required_categories = ["absorb", "create", "reflect"]
    
    for category in required_categories:
        if category not in path:
            raise ValueError(f"Growth path missing required category '{category}'")
        
        recommendations = path[category]
        if not isinstance(recommendations, list):
            raise ValueError(f"Growth path '{category}' must be a list")
        
        if len(recommendations) < 3 or len(recommendations) > 5:
            raise ValueError(
                f"Growth path '{category}' must have 3-5 recommendations, "
                f"got {len(recommendations)}"
            )
        
        for rec in recommendations:
            if "title" not in rec or "description" not in rec:
                raise ValueError(
                    f"Each recommendation in '{category}' must have 'title' and 'description'"
                )
    
    return True
