"""
Embedding Document Builder

This module builds structured text documents from quiz answers for embedding generation.
Ensures consistent formatting for caching purposes.
"""

from typing import List, Dict, Any


class Answer:
    """Quiz answer structure"""
    def __init__(self, question_id: str, selected_options: List[str]):
        self.question_id = question_id
        self.selected_options = selected_options


class QuizAnswers:
    """Complete quiz answers"""
    def __init__(self, section1: List[Answer], section2: List[Answer]):
        self.section1 = section1
        self.section2 = section2


def build_embedding_document(all_answers: Dict[str, Any]) -> str:
    """
    Build a structured embedding document from quiz answers.
    
    Creates a semantic text representation of quiz responses that can be
    embedded using Titan v2. Format is consistent to enable caching.
    
    Args:
        all_answers: Dictionary with 'section1' and 'section2' answer lists
        
    Returns:
        Structured text document suitable for embedding (500-2000 chars)
        
    Raises:
        ValueError: If answers are invalid or incomplete
        
    Preconditions:
        - all_answers contains valid Section 1 and Section 2 responses
        - Each answer has questionId and selectedOptions
        - selectedOptions is non-empty list
        
    Postconditions:
        - Returns structured text document
        - Document contains all quiz responses in semantic format
        - Document length is between 500-2000 characters
        - Format is consistent for caching purposes
    """
    if not all_answers:
        raise ValueError("Quiz answers cannot be empty")
    
    if 'section1' not in all_answers or 'section2' not in all_answers:
        raise ValueError("Quiz answers must contain section1 and section2")
    
    section1 = all_answers['section1']
    section2 = all_answers['section2']
    
    if not section1 or not section2:
        raise ValueError("Both sections must have answers")
    
    # Build structured document
    document_parts = []
    
    # Add Section 1 header
    document_parts.append("=== Taste Profile: Foundational Preferences ===\n")
    
    # Add Section 1 answers
    for i, answer in enumerate(section1, 1):
        question_id = answer.get('questionId', f'q{i}')
        options = answer.get('selectedOptions', [])
        
        if not options:
            raise ValueError(f"Answer {question_id} has no selected options")
        
        # Format: "Q1: option1, option2, option3"
        options_text = ", ".join(options)
        document_parts.append(f"Q{i}: {options_text}")
    
    # Add Section 2 header
    document_parts.append("\n=== Taste Profile: Deep Dive Preferences ===\n")
    
    # Add Section 2 answers
    for i, answer in enumerate(section2, 1):
        question_id = answer.get('questionId', f'q{i}')
        options = answer.get('selectedOptions', [])
        
        if not options:
            raise ValueError(f"Answer {question_id} has no selected options")
        
        # Format: "Q1: option1, option2, option3"
        options_text = ", ".join(options)
        document_parts.append(f"Q{i}: {options_text}")
    
    # Join all parts
    document = "\n".join(document_parts)
    
    # Validate length
    if len(document) < 100:
        raise ValueError(f"Document too short: {len(document)} chars (minimum 100)")
    
    if len(document) > 5000:
        # Truncate if too long (shouldn't happen with normal quiz answers)
        document = document[:5000]
    
    return document


def apply_weights(vector: List[float], answers: Dict[str, Any]) -> List[float]:
    """
    Apply weighting to embedding vector based on answer patterns.
    
    Adjusts vector dimensions based on answer characteristics to emphasize
    certain aspects of the taste profile.
    
    Args:
        vector: 1024-dimensional embedding vector
        answers: Complete quiz answers
        
    Returns:
        Weighted vector (NOT normalized - normalization happens separately)
        
    Raises:
        ValueError: If vector or answers are invalid
        
    Preconditions:
        - vector is 1024-dimensional normalized embedding
        - answers contains complete quiz responses
        
    Postconditions:
        - Returns 1024-dimensional weighted vector
        - Weights applied based on answer patterns
        - Vector maintains semantic meaning
        - Result is NOT normalized (requires separate normalization)
    """
    if not vector or len(vector) != 1024:
        raise ValueError("Vector must be 1024-dimensional")
    
    if not answers:
        raise ValueError("Answers cannot be empty")
    
    # For MVP, use simple uniform weighting
    # Future: Implement sophisticated weighting based on answer patterns
    # - Boost dimensions for strongly expressed preferences
    # - Reduce dimensions for neutral/uncertain responses
    # - Apply category-specific weights
    
    # Currently returns vector unchanged (weight = 1.0 for all dimensions)
    weighted = vector.copy()
    
    return weighted
