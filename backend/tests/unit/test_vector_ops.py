"""
Unit tests for vector operations (normalization, cosine similarity).

Tests the core vector math functions used for embedding processing and matching.
"""

import pytest
import math
from hypothesis import given, strategies as st
from hypothesis import assume


# Import the functions to test (adjust path as needed)
# from backend.src.utils.vector_ops import normalize_vector, cosine_similarity


# Mock implementations for demonstration (replace with actual imports)
def normalize_vector(vector):
    """Normalize a vector to unit length."""
    magnitude = math.sqrt(sum(v * v for v in vector))
    if magnitude == 0:
        raise ValueError("Cannot normalize zero vector")
    return [v / magnitude for v in vector]


def cosine_similarity(vec_a, vec_b):
    """Calculate cosine similarity between two vectors."""
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have same length")
    
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    return dot_product


# ============================================================================
# Unit Tests
# ============================================================================

class TestNormalizeVector:
    """Test suite for vector normalization."""
    
    def test_normalize_simple_vector(self):
        """Test normalization of a simple vector."""
        vector = [3.0, 4.0]
        normalized = normalize_vector(vector)
        
        # Check magnitude is 1.0
        magnitude = math.sqrt(sum(v * v for v in normalized))
        assert abs(magnitude - 1.0) < 0.0001
        
        # Check values
        assert abs(normalized[0] - 0.6) < 0.0001
        assert abs(normalized[1] - 0.8) < 0.0001
    
    def test_normalize_1024_vector(self):
        """Test normalization of 1024-dimensional vector."""
        vector = [0.5] * 1024
        normalized = normalize_vector(vector)
        
        # Check dimension
        assert len(normalized) == 1024
        
        # Check magnitude is 1.0
        magnitude = math.sqrt(sum(v * v for v in normalized))
        assert abs(magnitude - 1.0) < 0.0001
    
    def test_normalize_zero_vector_raises_error(self):
        """Test that normalizing zero vector raises error."""
        vector = [0.0] * 1024
        
        with pytest.raises(ValueError, match="Cannot normalize zero vector"):
            normalize_vector(vector)
    
    def test_normalize_preserves_direction(self):
        """Test that normalization preserves vector direction."""
        vector = [1.0, 2.0, 3.0]
        normalized = normalize_vector(vector)
        
        # All ratios should be preserved
        ratio_01 = normalized[0] / normalized[1]
        ratio_12 = normalized[1] / normalized[2]
        
        assert abs(ratio_01 - (1.0 / 2.0)) < 0.0001
        assert abs(ratio_12 - (2.0 / 3.0)) < 0.0001


class TestCosineSimilarity:
    """Test suite for cosine similarity calculation."""
    
    def test_identical_vectors_similarity_is_one(self):
        """Test that identical vectors have similarity 1.0."""
        vector = normalize_vector([1.0] * 1024)
        similarity = cosine_similarity(vector, vector)
        
        assert abs(similarity - 1.0) < 0.0001
    
    def test_orthogonal_vectors_similarity_is_zero(self):
        """Test that orthogonal vectors have similarity 0.0."""
        vec_a = [1.0, 0.0]
        vec_b = [0.0, 1.0]
        
        similarity = cosine_similarity(vec_a, vec_b)
        assert abs(similarity - 0.0) < 0.0001
    
    def test_opposite_vectors_similarity_is_negative_one(self):
        """Test that opposite vectors have similarity -1.0."""
        vec_a = normalize_vector([1.0] * 1024)
        vec_b = normalize_vector([-1.0] * 1024)
        
        similarity = cosine_similarity(vec_a, vec_b)
        assert abs(similarity - (-1.0)) < 0.0001
    
    def test_similarity_bounds(self):
        """Test that similarity is always between -1 and 1."""
        vec_a = normalize_vector([1.0, 2.0, 3.0])
        vec_b = normalize_vector([4.0, 5.0, 6.0])
        
        similarity = cosine_similarity(vec_a, vec_b)
        assert -1.0 <= similarity <= 1.0
    
    def test_different_length_vectors_raises_error(self):
        """Test that vectors of different lengths raise error."""
        vec_a = [1.0, 2.0]
        vec_b = [1.0, 2.0, 3.0]
        
        with pytest.raises(ValueError, match="Vectors must have same length"):
            cosine_similarity(vec_a, vec_b)


# ============================================================================
# Property-Based Tests
# ============================================================================

class TestVectorOpsProperties:
    """Property-based tests for vector operations."""
    
    @pytest.mark.property
    @given(st.lists(
        st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=1024,
        max_size=1024
    ))
    def test_normalization_produces_unit_vector(self, vector):
        """Property: Normalizing any non-zero vector produces unit length vector."""
        # Skip if vector is too close to zero
        magnitude = math.sqrt(sum(v * v for v in vector))
        assume(magnitude > 0.001)
        
        normalized = normalize_vector(vector)
        result_magnitude = math.sqrt(sum(v * v for v in normalized))
        
        assert abs(result_magnitude - 1.0) < 0.0001
    
    @pytest.mark.property
    @given(
        st.lists(
            st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False),
            min_size=1024,
            max_size=1024
        ),
        st.lists(
            st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False),
            min_size=1024,
            max_size=1024
        )
    )
    def test_cosine_similarity_bounds(self, vec_a, vec_b):
        """Property: Cosine similarity is always between -1 and 1."""
        # Normalize vectors first
        mag_a = math.sqrt(sum(v * v for v in vec_a))
        mag_b = math.sqrt(sum(v * v for v in vec_b))
        assume(mag_a > 0.001 and mag_b > 0.001)
        
        norm_a = normalize_vector(vec_a)
        norm_b = normalize_vector(vec_b)
        
        similarity = cosine_similarity(norm_a, norm_b)
        
        assert -1.0 <= similarity <= 1.0
    
    @pytest.mark.property
    @given(st.lists(
        st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        min_size=1024,
        max_size=1024
    ))
    def test_vector_similarity_with_itself_is_one(self, vector):
        """Property: Any vector has similarity 1.0 with itself."""
        magnitude = math.sqrt(sum(v * v for v in vector))
        assume(magnitude > 0.001)
        
        normalized = normalize_vector(vector)
        similarity = cosine_similarity(normalized, normalized)
        
        assert abs(similarity - 1.0) < 0.0001
