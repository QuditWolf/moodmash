"""
Vector Operations Utilities

Provides core vector operations for embedding manipulation:
- Vector normalization to unit length
- Cosine similarity calculation
- Vector validation
"""

import numpy as np
from typing import List, Union
import logging

logger = logging.getLogger(__name__)


def normalize_vector(vector: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    Normalize a vector to unit length (magnitude = 1.0).
    
    Args:
        vector: Input vector as list or numpy array
        
    Returns:
        Normalized vector as numpy array with magnitude ~1.0
        
    Raises:
        ValueError: If vector is empty or all zeros
        
    Example:
        >>> v = [3.0, 4.0]
        >>> normalized = normalize_vector(v)
        >>> np.linalg.norm(normalized)  # Should be ~1.0
        1.0
    """
    if not isinstance(vector, np.ndarray):
        vector = np.array(vector, dtype=np.float64)
    
    if len(vector) == 0:
        raise ValueError("Cannot normalize empty vector")
    
    # Calculate magnitude (L2 norm)
    magnitude = np.linalg.norm(vector)
    
    if magnitude == 0.0:
        raise ValueError("Cannot normalize zero vector")
    
    # Normalize to unit length
    normalized = vector / magnitude
    
    # Verify normalization (magnitude should be ~1.0 within tolerance)
    result_magnitude = np.linalg.norm(normalized)
    if not np.isclose(result_magnitude, 1.0, atol=0.0001):
        logger.warning(
            f"Normalized vector magnitude {result_magnitude} not close to 1.0"
        )
    
    return normalized


def cosine_similarity(
    vector1: Union[List[float], np.ndarray],
    vector2: Union[List[float], np.ndarray]
) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Cosine similarity is the dot product of normalized vectors,
    resulting in a value between -1 and 1:
    - 1.0: Identical vectors
    - 0.0: Orthogonal vectors
    - -1.0: Opposite vectors
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        Cosine similarity score between -1.0 and 1.0
        
    Raises:
        ValueError: If vectors have different dimensions
        
    Example:
        >>> v1 = [1.0, 0.0, 0.0]
        >>> v2 = [1.0, 0.0, 0.0]
        >>> cosine_similarity(v1, v2)
        1.0
    """
    if not isinstance(vector1, np.ndarray):
        vector1 = np.array(vector1, dtype=np.float64)
    if not isinstance(vector2, np.ndarray):
        vector2 = np.array(vector2, dtype=np.float64)
    
    if len(vector1) != len(vector2):
        raise ValueError(
            f"Vectors must have same dimensions: {len(vector1)} != {len(vector2)}"
        )
    
    # Normalize both vectors
    norm1 = normalize_vector(vector1)
    norm2 = normalize_vector(vector2)
    
    # Calculate dot product of normalized vectors
    similarity = np.dot(norm1, norm2)
    
    # Ensure result is within valid bounds [-1, 1]
    # (floating point errors can cause slight overflow)
    similarity = np.clip(similarity, -1.0, 1.0)
    
    return float(similarity)


def validate_vector(
    vector: Union[List[float], np.ndarray],
    expected_dim: int = 1024,
    check_normalized: bool = False
) -> bool:
    """
    Validate vector dimensions and properties.
    
    Args:
        vector: Vector to validate
        expected_dim: Expected number of dimensions (default: 1024 for Titan v2)
        check_normalized: If True, verify vector is normalized to unit length
        
    Returns:
        True if vector is valid
        
    Raises:
        ValueError: If vector is invalid with descriptive error message
        
    Example:
        >>> v = np.random.rand(1024)
        >>> validate_vector(v, expected_dim=1024)
        True
    """
    if not isinstance(vector, np.ndarray):
        vector = np.array(vector, dtype=np.float64)
    
    # Check dimensions
    if len(vector) != expected_dim:
        raise ValueError(
            f"Vector has {len(vector)} dimensions, expected {expected_dim}"
        )
    
    # Check for NaN or Inf values
    if np.any(np.isnan(vector)):
        raise ValueError("Vector contains NaN values")
    
    if np.any(np.isinf(vector)):
        raise ValueError("Vector contains Inf values")
    
    # Check if normalized (if requested)
    if check_normalized:
        magnitude = np.linalg.norm(vector)
        if not np.isclose(magnitude, 1.0, atol=0.0001):
            raise ValueError(
                f"Vector is not normalized: magnitude = {magnitude}, expected ~1.0"
            )
    
    return True


def apply_weights(
    vector: Union[List[float], np.ndarray],
    weights: Union[List[float], np.ndarray]
) -> np.ndarray:
    """
    Apply element-wise weights to a vector.
    
    This is used to emphasize certain dimensions of the embedding
    based on answer patterns or importance scores.
    
    Args:
        vector: Input vector
        weights: Weight vector (same dimensions as input)
        
    Returns:
        Weighted vector (not normalized)
        
    Raises:
        ValueError: If dimensions don't match
        
    Example:
        >>> v = np.array([1.0, 2.0, 3.0])
        >>> w = np.array([2.0, 1.0, 0.5])
        >>> apply_weights(v, w)
        array([2.0, 2.0, 1.5])
    """
    if not isinstance(vector, np.ndarray):
        vector = np.array(vector, dtype=np.float64)
    if not isinstance(weights, np.ndarray):
        weights = np.array(weights, dtype=np.float64)
    
    if len(vector) != len(weights):
        raise ValueError(
            f"Vector and weights must have same dimensions: "
            f"{len(vector)} != {len(weights)}"
        )
    
    # Apply element-wise multiplication
    weighted = vector * weights
    
    return weighted
