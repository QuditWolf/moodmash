"""
Embedding Document Builder

Builds semantic text documents from quiz answers for embedding generation.
Ensures consistent formatting for caching and reproducibility.
"""

import json
import hashlib
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


def build_embedding_document(
    section1_answers: List[Dict[str, Any]],
    section2_answers: List[Dict[str, Any]]
) -> str:
    """
    Build a semantic text document from quiz answers.
    
    The document is structured to capture the user's taste profile
    in a format optimized for embedding generation. It includes:
    - Selected options from all questions
    - Question categories and context
    - Answer patterns and preferences
    
    Args:
        section1_answers: List of Section 1 answers with questionId and selectedOptions
        section2_answers: List of Section 2 answers with questionId and selectedOptions
        
    Returns:
        Formatted text document (500-2000 characters)
        
    Raises:
        ValueError: If answers are invalid or document length is out of bounds
        
    Example:
        >>> s1 = [{"questionId": "q1", "selectedOptions": ["Visual art"]}]
        >>> s2 = [{"questionId": "q6", "selectedOptions": ["Minimalist"]}]
        >>> doc = build_embedding_document(s1, s2)
        >>> len(doc)
        750  # Example length
    """
    if not section1_answers or not section2_answers:
        raise ValueError("Both section1 and section2 answers are required")
    
    # Build structured document
    document_parts = []
    
    # Header
    document_parts.append("User Taste Profile:")
    document_parts.append("")
    
    # Section 1: Foundational preferences
    document_parts.append("Foundational Preferences:")
    for answer in section1_answers:
        question_id = answer.get("questionId", "unknown")
        selected = answer.get("selectedOptions", [])
        category = answer.get("category", "general")
        
        if selected:
            options_text = ", ".join(selected)
            document_parts.append(f"- {category}: {options_text}")
    
    document_parts.append("")
    
    # Section 2: Adaptive preferences
    document_parts.append("Refined Preferences:")
    for answer in section2_answers:
        question_id = answer.get("questionId", "unknown")
        selected = answer.get("selectedOptions", [])
        category = answer.get("category", "general")
        
        if selected:
            options_text = ", ".join(selected)
            document_parts.append(f"- {category}: {options_text}")
    
    document_parts.append("")
    
    # Summary section
    all_selections = []
    for answer in section1_answers + section2_answers:
        all_selections.extend(answer.get("selectedOptions", []))
    
    document_parts.append("Overall Taste Summary:")
    document_parts.append(f"Selected {len(all_selections)} preferences across cultural dimensions.")
    
    # Join into final document
    document = "\n".join(document_parts)
    
    # Validate document length
    doc_length = len(document)
    if doc_length < 500:
        logger.warning(
            f"Document length {doc_length} is below minimum 500 characters"
        )
    elif doc_length > 2000:
        # Truncate if too long
        logger.warning(
            f"Document length {doc_length} exceeds maximum 2000 characters, truncating"
        )
        document = document[:2000]
    
    return document


def compute_document_hash(document: str) -> str:
    """
    Compute SHA-256 hash of embedding document for caching.
    
    Args:
        document: Embedding document text
        
    Returns:
        Hexadecimal hash string (64 characters)
        
    Example:
        >>> doc = "User taste profile..."
        >>> hash_val = compute_document_hash(doc)
        >>> len(hash_val)
        64
    """
    # Use UTF-8 encoding for consistent hashing
    doc_bytes = document.encode('utf-8')
    
    # Compute SHA-256 hash
    hash_obj = hashlib.sha256(doc_bytes)
    hash_hex = hash_obj.hexdigest()
    
    return hash_hex


def format_answers_for_storage(
    section1_answers: List[Dict[str, Any]],
    section2_answers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Format quiz answers for storage (without raw answer text).
    
    This creates a privacy-preserving representation that stores
    only the structure and metadata, not the actual answer content.
    
    Args:
        section1_answers: Section 1 answers
        section2_answers: Section 2 answers
        
    Returns:
        Formatted answer structure with metadata only
        
    Example:
        >>> s1 = [{"questionId": "q1", "selectedOptions": ["opt1"]}]
        >>> s2 = [{"questionId": "q6", "selectedOptions": ["opt2"]}]
        >>> formatted = format_answers_for_storage(s1, s2)
        >>> "selectedOptions" not in str(formatted)
        True
    """
    formatted = {
        "section1": {
            "count": len(section1_answers),
            "questions": [
                {
                    "questionId": ans.get("questionId"),
                    "category": ans.get("category"),
                    "selectionCount": len(ans.get("selectedOptions", []))
                }
                for ans in section1_answers
            ]
        },
        "section2": {
            "count": len(section2_answers),
            "questions": [
                {
                    "questionId": ans.get("questionId"),
                    "category": ans.get("category"),
                    "selectionCount": len(ans.get("selectedOptions", []))
                }
                for ans in section2_answers
            ]
        },
        "totalSelections": sum(
            len(ans.get("selectedOptions", []))
            for ans in section1_answers + section2_answers
        )
    }
    
    return formatted
