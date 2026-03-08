"""
Vector Operations Utilities

This module provides vector operations for embedding manipulation and similarity calculation.
Includes normalization and cosine similarity functions.
"""

import math
from typing import List


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.
    
    Calculates the magnitude (L2 norm) of the vector and divides each element
    by the magnitude to produce a unit vector.
    
    Args:
        vector: List of float values representing the vector
        
    Returns:
        Normalized vector with magnitude approximately 1.0
        
    Raises:
        ValueError: If vector is empty or has zero magnitude
        
    Preconditions:
        - vector is non-empty list of numbers
        - vector is not zero vector (magnitude > 0)
        
    Postconditions:
        - Returns list of same length as input
        - Resulting vector has unit length (magnitude = 1.0 within 0.0001 tolerance)
        - Direction preserved from original vector
        - No mutations to input vector
    """
    if not vector:
        raise ValueError("Cannot normalize empty vector")
    
    # Calculate magnitude (L2 norm)
    magnitude = math.sqrt(sum(v * v for v in vector))
    
    if magnitude == 0:
        raise ValueError("Cannot normalize zero vector")
    
    # Normalize by dividing each element by magnitude
    normalized = [v / magnitude for v in vector]
    
    return normalized


def cosine_similarity(vector_a: List[float], vector_b: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Computes the dot product of two normalized vectors, which equals the cosine
    of the angle between them. Result ranges from -1 (opposite) to 1 (identical).
    
    Args:
        vector_a: First normalized vector
        vector_b: Second normalized vector
        
    Returns:
        Cosine similarity score between -1 and 1
        
    Raises:
        ValueError: If vectors have different lengths
        
    Preconditions:
        - vector_a and vector_b are non-null lists
        - vector_a.length == vector_b.length
        - Vectors are normalized (unit length)
        
    Postconditions:
        - Returns float between -1 and 1
        - Result represents cosine of angle between vectors
        - Higher values indicate greater similarity
        - 1.0 means identical vectors, 0.0 means orthogonal, -1.0 means opposite
    """
    if len(vector_a) != len(vector_b):
        raise ValueError(
            f"Vectors must have same length: {len(vector_a)} != {len(vector_b)}"
        )
    
    if not vector_a:
        raise ValueError("Cannot calculate similarity of empty vectors")
    
    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    
    # Clamp to valid range to handle floating point errors
    # (normalized vectors should naturally produce values in [-1, 1])
    similarity = max(-1.0, min(1.0, dot_product))
    
    return similarity


def validate_vector(vector: List[float], expected_dimension: int = 1024) -> bool:
    """
    Validate that a vector meets requirements.
    
    Checks that vector has correct dimensions and all values are in valid range.
    
    Args:
        vector: Vector to validate
        expected_dimension: Expected number of dimensions (default 1024 for Titan v2)
        
    Returns:
        True if vector is valid
        
    Raises:
        ValueError: If vector is invalid with specific error message
    """
    if not isinstance(vector, list):
        raise ValueError("Vector must be a list")
    
    if len(vector) != expected_dimension:
        raise ValueError(
            f"Vector must have {expected_dimension} dimensions, got {len(vector)}"
        )
    
    for i, value in enumerate(vector):
        if not isinstance(value, (int, float)):
            raise ValueError(f"Vector element {i} must be numeric, got {type(value)}")
        
        if not (-1 <= value <= 1):
            raise ValueError(
                f"Vector element {i} must be between -1 and 1, got {value}"
            )
    
    return True
