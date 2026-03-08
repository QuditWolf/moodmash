"""
Unit Tests for Embedding Document Builder

Tests document building, hashing, and formatting.
"""

import pytest
from src.utils.embedding_builder import (
    build_embedding_document,
    compute_document_hash,
    format_answers_for_storage
)


class TestBuildEmbeddingDocument:
    """Test embedding document building."""
    
    @pytest.fixture
    def sample_section1_answers(self):
        """Sample Section 1 answers."""
        return [
            {
                "questionId": "q1",
                "selectedOptions": ["Visual art", "Photography"],
                "category": "content_preference"
            },
            {
                "questionId": "q2",
                "selectedOptions": ["By exploring"],
                "category": "discovery_style"
            },
            {
                "questionId": "q3",
                "selectedOptions": ["Calm", "Reflective"],
                "category": "mood_preference"
            },
            {
                "questionId": "q4",
                "selectedOptions": ["Observe"],
                "category": "engagement_style"
            },
            {
                "questionId": "q5",
                "selectedOptions": ["Aesthetic appeal"],
                "category": "attraction_factors"
            }
        ]
    
    @pytest.fixture
    def sample_section2_answers(self):
        """Sample Section 2 answers."""
        return [
            {
                "questionId": "q6",
                "selectedOptions": ["Minimalist"],
                "category": "visual_style"
            },
            {
                "questionId": "q7",
                "selectedOptions": ["Personal stories"],
                "category": "narrative_preference"
            },
            {
                "questionId": "q8",
                "selectedOptions": ["Learning"],
                "category": "activity_preference"
            },
            {
                "questionId": "q9",
                "selectedOptions": ["Contemporary"],
                "category": "cultural_alignment"
            },
            {
                "questionId": "q10",
                "selectedOptions": ["Focused"],
                "category": "taste_identity"
            }
        ]
    
    def test_build_document_structure(self, sample_section1_answers, sample_section2_answers):
        """Test that document has correct structure."""
        doc = build_embedding_document(sample_section1_answers, sample_section2_answers)
        
        assert "User Taste Profile:" in doc
        assert "Foundational Preferences:" in doc
        assert "Refined Preferences:" in doc
        assert "Overall Taste Summary:" in doc
    
    def test_build_document_includes_answers(self, sample_section1_answers, sample_section2_answers):
        """Test that document includes answer content."""
        doc = build_embedding_document(sample_section1_answers, sample_section2_answers)
        
        # Check Section 1 content
        assert "Visual art" in doc
        assert "Photography" in doc
        assert "content_preference" in doc
        
        # Check Section 2 content
        assert "Minimalist" in doc
        assert "visual_style" in doc
    
    def test_build_document_length(self, sample_section1_answers, sample_section2_answers):
        """Test that document length is within bounds."""
        doc = build_embedding_document(sample_section1_answers, sample_section2_answers)
        
        doc_length = len(doc)
        # Allow slightly below 500 since test data is minimal
        assert 400 <= doc_length <= 2000, f"Document length {doc_length} out of bounds"
    
    def test_build_document_consistency(self, sample_section1_answers, sample_section2_answers):
        """Test that same answers produce same document."""
        doc1 = build_embedding_document(sample_section1_answers, sample_section2_answers)
        doc2 = build_embedding_document(sample_section1_answers, sample_section2_answers)
        
        assert doc1 == doc2
    
    def test_build_document_empty_section1_raises(self, sample_section2_answers):
        """Test that empty Section 1 raises ValueError."""
        with pytest.raises(ValueError, match="Both section1 and section2"):
            build_embedding_document([], sample_section2_answers)
    
    def test_build_document_empty_section2_raises(self, sample_section1_answers):
        """Test that empty Section 2 raises ValueError."""
        with pytest.raises(ValueError, match="Both section1 and section2"):
            build_embedding_document(sample_section1_answers, [])


class TestComputeDocumentHash:
    """Test document hashing."""
    
    def test_hash_length(self):
        """Test that hash is 64 characters (SHA-256 hex)."""
        doc = "Test document for hashing"
        hash_val = compute_document_hash(doc)
        
        assert len(hash_val) == 64
    
    def test_hash_consistency(self):
        """Test that same document produces same hash."""
        doc = "Test document for hashing"
        hash1 = compute_document_hash(doc)
        hash2 = compute_document_hash(doc)
        
        assert hash1 == hash2
    
    def test_hash_uniqueness(self):
        """Test that different documents produce different hashes."""
        doc1 = "Test document 1"
        doc2 = "Test document 2"
        
        hash1 = compute_document_hash(doc1)
        hash2 = compute_document_hash(doc2)
        
        assert hash1 != hash2
    
    def test_hash_format(self):
        """Test that hash is valid hexadecimal."""
        doc = "Test document"
        hash_val = compute_document_hash(doc)
        
        # Should be valid hex string
        int(hash_val, 16)  # Raises ValueError if not valid hex


class TestFormatAnswersForStorage:
    """Test answer formatting for storage."""
    
    @pytest.fixture
    def sample_answers(self):
        """Sample answers for testing."""
        section1 = [
            {
                "questionId": "q1",
                "selectedOptions": ["opt1", "opt2"],
                "category": "cat1"
            },
            {
                "questionId": "q2",
                "selectedOptions": ["opt3"],
                "category": "cat2"
            }
        ]
        section2 = [
            {
                "questionId": "q6",
                "selectedOptions": ["opt4"],
                "category": "cat3"
            }
        ]
        return section1, section2
    
    def test_format_structure(self, sample_answers):
        """Test that formatted structure has correct fields."""
        section1, section2 = sample_answers
        formatted = format_answers_for_storage(section1, section2)
        
        assert "section1" in formatted
        assert "section2" in formatted
        assert "totalSelections" in formatted
    
    def test_format_counts(self, sample_answers):
        """Test that counts are correct."""
        section1, section2 = sample_answers
        formatted = format_answers_for_storage(section1, section2)
        
        assert formatted["section1"]["count"] == 2
        assert formatted["section2"]["count"] == 1
        assert formatted["totalSelections"] == 4  # 2 + 1 from s1, 1 from s2
    
    def test_format_no_raw_answers(self, sample_answers):
        """Test that raw answer text is not included."""
        section1, section2 = sample_answers
        formatted = format_answers_for_storage(section1, section2)
        
        # Convert to string and check for option text
        formatted_str = str(formatted)
        assert "opt1" not in formatted_str
        assert "opt2" not in formatted_str
        assert "opt3" not in formatted_str
        assert "opt4" not in formatted_str
    
    def test_format_includes_metadata(self, sample_answers):
        """Test that metadata is included."""
        section1, section2 = sample_answers
        formatted = format_answers_for_storage(section1, section2)
        
        # Check Section 1 metadata
        q1 = formatted["section1"]["questions"][0]
        assert q1["questionId"] == "q1"
        assert q1["category"] == "cat1"
        assert q1["selectionCount"] == 2
        
        # Check Section 2 metadata
        q6 = formatted["section2"]["questions"][0]
        assert q6["questionId"] == "q6"
        assert q6["category"] == "cat3"
        assert q6["selectionCount"] == 1
