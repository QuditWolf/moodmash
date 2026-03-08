"""
Unit Tests for Vector Operations

Tests vector normalization, cosine similarity, and validation.
"""

import pytest
import numpy as np
from src.utils.vector_ops import (
    normalize_vector,
    cosine_similarity,
    validate_vector,
    apply_weights
)


class TestNormalizeVector:
    """Test vector normalization functionality."""
    
    def test_normalize_simple_vector(self):
        """Test normalization of a simple 2D vector."""
        vector = [3.0, 4.0]
        normalized = normalize_vector(vector)
        
        # Check magnitude is 1.0
        magnitude = np.linalg.norm(normalized)
        assert np.isclose(magnitude, 1.0, atol=0.0001)
        
        # Check values are correct
        assert np.isclose(normalized[0], 0.6, atol=0.0001)
        assert np.isclose(normalized[1], 0.8, atol=0.0001)
    
    def test_normalize_already_normalized(self):
        """Test normalizing an already normalized vector."""
        vector = [1.0, 0.0, 0.0]
        normalized = normalize_vector(vector)
        
        magnitude = np.linalg.norm(normalized)
        assert np.isclose(magnitude, 1.0, atol=0.0001)
        assert np.allclose(normalized, vector)
    
    def test_normalize_high_dimensional(self):
        """Test normalization of 1024-dimensional vector."""
        vector = np.random.rand(1024)
        normalized = normalize_vector(vector)
        
        magnitude = np.linalg.norm(normalized)
        assert np.isclose(magnitude, 1.0, atol=0.0001)
    
    def test_normalize_empty_vector_raises(self):
        """Test that empty vector raises ValueError."""
        with pytest.raises(ValueError, match="Cannot normalize empty vector"):
            normalize_vector([])
    
    def test_normalize_zero_vector_raises(self):
        """Test that zero vector raises ValueError."""
        with pytest.raises(ValueError, match="Cannot normalize zero vector"):
            normalize_vector([0.0, 0.0, 0.0])
    
    def test_normalize_numpy_array(self):
        """Test normalization with numpy array input."""
        vector = np.array([3.0, 4.0])
        normalized = normalize_vector(vector)
        
        magnitude = np.linalg.norm(normalized)
        assert np.isclose(magnitude, 1.0, atol=0.0001)


class TestCosineSimilarity:
    """Test cosine similarity calculation."""
    
    def test_identical_vectors(self):
        """Test similarity of identical vectors is 1.0."""
        v1 = [1.0, 2.0, 3.0]
        v2 = [1.0, 2.0, 3.0]
        
        similarity = cosine_similarity(v1, v2)
        assert np.isclose(similarity, 1.0, atol=0.0001)
    
    def test_opposite_vectors(self):
        """Test similarity of opposite vectors is -1.0."""
        v1 = [1.0, 0.0, 0.0]
        v2 = [-1.0, 0.0, 0.0]
        
        similarity = cosine_similarity(v1, v2)
        assert np.isclose(similarity, -1.0, atol=0.0001)
    
    def test_orthogonal_vectors(self):
        """Test similarity of orthogonal vectors is 0.0."""
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.0, 1.0, 0.0]
        
        similarity = cosine_similarity(v1, v2)
        assert np.isclose(similarity, 0.0, atol=0.0001)
    
    def test_similarity_bounds(self):
        """Test that similarity is always between -1 and 1."""
        for _ in range(100):
            v1 = np.random.rand(128)
            v2 = np.random.rand(128)
            
            similarity = cosine_similarity(v1, v2)
            assert -1.0 <= similarity <= 1.0
    
    def test_different_dimensions_raises(self):
        """Test that different dimensions raise ValueError."""
        v1 = [1.0, 2.0, 3.0]
        v2 = [1.0, 2.0]
        
        with pytest.raises(ValueError, match="same dimensions"):
            cosine_similarity(v1, v2)
    
    def test_high_dimensional_similarity(self):
        """Test similarity with 1024-dimensional vectors."""
        v1 = np.random.rand(1024)
        v2 = v1 + np.random.rand(1024) * 0.1  # Similar but not identical
        
        similarity = cosine_similarity(v1, v2)
        assert 0.9 < similarity < 1.0  # Should be high similarity


class TestValidateVector:
    """Test vector validation."""
    
    def test_valid_vector(self):
        """Test validation of valid 1024-dim vector."""
        vector = np.random.rand(1024)
        assert validate_vector(vector, expected_dim=1024)
    
    def test_wrong_dimensions_raises(self):
        """Test that wrong dimensions raise ValueError."""
        vector = np.random.rand(512)
        
        with pytest.raises(ValueError, match="512 dimensions, expected 1024"):
            validate_vector(vector, expected_dim=1024)
    
    def test_nan_values_raises(self):
        """Test that NaN values raise ValueError."""
        vector = np.random.rand(1024)
        vector[0] = np.nan
        
        with pytest.raises(ValueError, match="contains NaN"):
            validate_vector(vector)
    
    def test_inf_values_raises(self):
        """Test that Inf values raise ValueError."""
        vector = np.random.rand(1024)
        vector[0] = np.inf
        
        with pytest.raises(ValueError, match="contains Inf"):
            validate_vector(vector)
    
    def test_check_normalized(self):
        """Test validation of normalized vector."""
        vector = np.random.rand(1024)
        normalized = normalize_vector(vector)
        
        assert validate_vector(normalized, check_normalized=True)
    
    def test_check_normalized_fails(self):
        """Test that non-normalized vector fails check."""
        vector = np.random.rand(1024) * 10  # Not normalized
        
        with pytest.raises(ValueError, match="not normalized"):
            validate_vector(vector, check_normalized=True)


class TestApplyWeights:
    """Test weight application to vectors."""
    
    def test_apply_uniform_weights(self):
        """Test applying uniform weights (no change)."""
        vector = np.array([1.0, 2.0, 3.0])
        weights = np.array([1.0, 1.0, 1.0])
        
        weighted = apply_weights(vector, weights)
        assert np.allclose(weighted, vector)
    
    def test_apply_scaling_weights(self):
        """Test applying scaling weights."""
        vector = np.array([1.0, 2.0, 3.0])
        weights = np.array([2.0, 1.0, 0.5])
        
        weighted = apply_weights(vector, weights)
        expected = np.array([2.0, 2.0, 1.5])
        assert np.allclose(weighted, expected)
    
    def test_apply_zero_weights(self):
        """Test applying zero weights."""
        vector = np.array([1.0, 2.0, 3.0])
        weights = np.array([0.0, 0.0, 0.0])
        
        weighted = apply_weights(vector, weights)
        assert np.allclose(weighted, np.zeros(3))
    
    def test_different_dimensions_raises(self):
        """Test that different dimensions raise ValueError."""
        vector = np.array([1.0, 2.0, 3.0])
        weights = np.array([1.0, 1.0])
        
        with pytest.raises(ValueError, match="same dimensions"):
            apply_weights(vector, weights)
    
    def test_high_dimensional_weights(self):
        """Test applying weights to 1024-dim vector."""
        vector = np.random.rand(1024)
        weights = np.random.rand(1024)
        
        weighted = apply_weights(vector, weights)
        assert len(weighted) == 1024
        assert np.allclose(weighted, vector * weights)
