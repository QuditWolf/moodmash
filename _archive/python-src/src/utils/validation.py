"""
Input Validation Utilities

This module provides validation functions for quiz answers, IDs, and vectors.
"""

import re
from typing import List, Dict, Any


# UUID regex pattern (RFC 4122)
UUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)


def validate_uuid(value: str, field_name: str = "ID") -> bool:
    """
    Validate that a string is a valid UUID format.
    
    Args:
        value: String to validate
        field_name: Name of field for error messages
        
    Returns:
        True if valid UUID
        
    Raises:
        ValueError: If not a valid UUID with descriptive message
    """
    if not value:
        raise ValueError(f"{field_name} cannot be empty")
    
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    
    if not UUID_PATTERN.match(value):
        raise ValueError(f"{field_name} must be a valid UUID format")
    
    return True


def validate_section1_answers(answers: List[Dict[str, Any]]) -> bool:
    """
    Validate Section 1 answers.
    
    Checks that exactly 5 answers are provided with correct structure.
    
    Args:
        answers: List of answer dictionaries
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails with specific error message
    """
    if not answers:
        raise ValueError("Section 1 answers cannot be empty")
    
    if not isinstance(answers, list):
        raise ValueError("Section 1 answers must be a list")
    
    if len(answers) != 5:
        raise ValueError(f"Section 1 must have exactly 5 answers, got {len(answers)}")
    
    # Validate each answer
    for i, answer in enumerate(answers, 1):
        validate_answer_structure(answer, f"Section 1 answer {i}")
    
    return True


def validate_answer_structure(answer: Dict[str, Any], context: str = "Answer") -> bool:
    """
    Validate the structure of a single answer.
    
    Checks that answer has questionId and selectedOptions with at least one option.
    
    Args:
        answer: Answer dictionary to validate
        context: Context string for error messages
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails with specific error message
    """
    if not isinstance(answer, dict):
        raise ValueError(f"{context} must be a dictionary")
    
    # Check questionId
    if 'questionId' not in answer:
        raise ValueError(f"{context} must have questionId field")
    
    question_id = answer['questionId']
    if not question_id or not isinstance(question_id, str):
        raise ValueError(f"{context} questionId must be a non-empty string")
    
    # Check selectedOptions
    if 'selectedOptions' not in answer:
        raise ValueError(f"{context} must have selectedOptions field")
    
    selected_options = answer['selectedOptions']
    if not isinstance(selected_options, list):
        raise ValueError(f"{context} selectedOptions must be a list")
    
    if len(selected_options) == 0:
        raise ValueError(f"{context} must have at least one selected option")
    
    # Validate each option
    for j, option in enumerate(selected_options):
        if not isinstance(option, str):
            raise ValueError(f"{context} option {j} must be a string")
        
        if len(option) > 500:
            raise ValueError(
                f"{context} option {j} exceeds maximum length of 500 characters"
            )
    
    return True


def validate_quiz_answers(all_answers: Dict[str, Any]) -> bool:
    """
    Validate complete quiz answers.
    
    Checks that both Section 1 and Section 2 answers are present and valid.
    
    Args:
        all_answers: Dictionary with section1 and section2 answer lists
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails with specific error message
    """
    if not all_answers:
        raise ValueError("Quiz answers cannot be empty")
    
    if not isinstance(all_answers, dict):
        raise ValueError("Quiz answers must be a dictionary")
    
    # Check section1
    if 'section1' not in all_answers:
        raise ValueError("Quiz answers must contain section1")
    
    validate_section1_answers(all_answers['section1'])
    
    # Check section2
    if 'section2' not in all_answers:
        raise ValueError("Quiz answers must contain section2")
    
    section2 = all_answers['section2']
    if not isinstance(section2, list):
        raise ValueError("Section 2 answers must be a list")
    
    if len(section2) < 1:
        raise ValueError("Section 2 must have at least 1 answer")
    
    # Validate each Section 2 answer
    for i, answer in enumerate(section2, 1):
        validate_answer_structure(answer, f"Section 2 answer {i}")
    
    return True


def validate_vector(vector: List[float], expected_dimension: int = 1024) -> bool:
    """
    Validate embedding vector.
    
    Checks dimensions and value bounds.
    
    Args:
        vector: Vector to validate
        expected_dimension: Expected number of dimensions (default 1024)
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If validation fails with specific error message
    """
    if not vector:
        raise ValueError("Vector cannot be empty")
    
    if not isinstance(vector, list):
        raise ValueError("Vector must be a list")
    
    if len(vector) != expected_dimension:
        raise ValueError(
            f"Vector must have {expected_dimension} dimensions, got {len(vector)}"
        )
    
    # Check each value
    for i, value in enumerate(vector):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Vector element {i} must be numeric")
        
        if not (-1 <= value <= 1):
            raise ValueError(
                f"Vector element {i} must be between -1 and 1, got {value}"
            )
    
    return True
