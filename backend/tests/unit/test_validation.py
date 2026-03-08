"""
Unit Tests for Validation Utilities

Tests input validation for quiz answers, IDs, and data structures.
"""

import pytest
import uuid
from src.utils.validation import (
    validate_uuid,
    validate_quiz_answers,
    validate_section1_answers,
    validate_section2_answers,
    validate_answer_structure,
    validate_user_id,
    validate_session_id,
    validate_taste_dna,
    validate_growth_path
)


class TestValidateUUID:
    """Test UUID validation."""
    
    def test_valid_uuid(self):
        """Test validation of valid UUID."""
        valid_uuid = str(uuid.uuid4())
        assert validate_uuid(valid_uuid)
    
    def test_invalid_uuid_raises(self):
        """Test that invalid UUID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid id"):
            validate_uuid("not-a-uuid")
    
    def test_empty_string_raises(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError):
            validate_uuid("")
    
    def test_custom_field_name(self):
        """Test custom field name in error message."""
        with pytest.raises(ValueError, match="Invalid sessionId"):
            validate_uuid("invalid", field_name="sessionId")


class TestValidateQuizAnswers:
    """Test quiz answer validation."""
    
    @pytest.fixture
    def valid_answers(self):
        """Valid quiz answers."""
        return [
            {
                "questionId": "q1",
                "selectedOptions": ["option1"],
                "category": "test"
            },
            {
                "questionId": "q2",
                "selectedOptions": ["option2", "option3"],
                "category": "test"
            },
            {
                "questionId": "q3",
                "selectedOptions": ["option4"],
                "category": "test"
            },
            {
                "questionId": "q4",
                "selectedOptions": ["option5"],
                "category": "test"
            },
            {
                "questionId": "q5",
                "selectedOptions": ["option6"],
                "category": "test"
            }
        ]
    
    def test_valid_answers(self, valid_answers):
        """Test validation of valid answers."""
        assert validate_quiz_answers(valid_answers, expected_count=5)
    
    def test_wrong_count_raises(self, valid_answers):
        """Test that wrong answer count raises ValueError."""
        with pytest.raises(ValueError, match="exactly 5 answers"):
            validate_quiz_answers(valid_answers[:3], expected_count=5)
    
    def test_missing_question_id_raises(self, valid_answers):
        """Test that missing questionId raises ValueError."""
        invalid = valid_answers.copy()
        del invalid[0]["questionId"]
        
        with pytest.raises(ValueError, match="missing required field 'questionId'"):
            validate_quiz_answers(invalid)
    
    def test_missing_selected_options_raises(self, valid_answers):
        """Test that missing selectedOptions raises ValueError."""
        invalid = valid_answers.copy()
        del invalid[0]["selectedOptions"]
        
        with pytest.raises(ValueError, match="missing required field 'selectedOptions'"):
            validate_quiz_answers(invalid)
    
    def test_empty_selected_options_raises(self, valid_answers):
        """Test that empty selectedOptions raises ValueError."""
        invalid = valid_answers.copy()
        invalid[0]["selectedOptions"] = []
        
        with pytest.raises(ValueError, match="at least one selected option"):
            validate_quiz_answers(invalid)
    
    def test_non_list_selected_options_raises(self, valid_answers):
        """Test that non-list selectedOptions raises ValueError."""
        invalid = valid_answers.copy()
        invalid[0]["selectedOptions"] = "not a list"
        
        with pytest.raises(ValueError, match="must be a list"):
            validate_quiz_answers(invalid)
    
    def test_non_string_option_raises(self, valid_answers):
        """Test that non-string option raises ValueError."""
        invalid = valid_answers.copy()
        invalid[0]["selectedOptions"] = [123]
        
        with pytest.raises(ValueError, match="must be a string"):
            validate_quiz_answers(invalid)
    
    def test_too_long_option_raises(self, valid_answers):
        """Test that option exceeding 500 chars raises ValueError."""
        invalid = valid_answers.copy()
        invalid[0]["selectedOptions"] = ["x" * 501]
        
        with pytest.raises(ValueError, match="exceeds 500 characters"):
            validate_quiz_answers(invalid)
    
    def test_empty_option_raises(self, valid_answers):
        """Test that empty option string raises ValueError."""
        invalid = valid_answers.copy()
        invalid[0]["selectedOptions"] = ["   "]
        
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_quiz_answers(invalid)


class TestValidateSection1Answers:
    """Test Section 1 answer validation."""
    
    def test_valid_section1(self):
        """Test validation of valid Section 1 answers."""
        answers = [
            {"questionId": f"q{i}", "selectedOptions": ["opt"]}
            for i in range(1, 6)
        ]
        assert validate_section1_answers(answers)
    
    def test_wrong_count_raises(self):
        """Test that wrong count raises ValueError with Section 1 in message."""
        answers = [
            {"questionId": "q1", "selectedOptions": ["opt"]}
        ]
        with pytest.raises(ValueError, match="Section 1"):
            validate_section1_answers(answers)


class TestValidateSection2Answers:
    """Test Section 2 answer validation."""
    
    def test_valid_section2(self):
        """Test validation of valid Section 2 answers."""
        answers = [
            {"questionId": f"q{i}", "selectedOptions": ["opt"]}
            for i in range(6, 11)
        ]
        assert validate_section2_answers(answers)
    
    def test_wrong_count_raises(self):
        """Test that wrong count raises ValueError with Section 2 in message."""
        answers = [
            {"questionId": "q6", "selectedOptions": ["opt"]}
        ]
        with pytest.raises(ValueError, match="Section 2"):
            validate_section2_answers(answers)


class TestValidateAnswerStructure:
    """Test individual answer structure validation."""
    
    def test_valid_answer(self):
        """Test validation of valid answer."""
        answer = {
            "questionId": "q1",
            "selectedOptions": ["option1"]
        }
        assert validate_answer_structure(answer)
    
    def test_missing_field_raises(self):
        """Test that missing field raises ValueError."""
        answer = {"questionId": "q1"}
        with pytest.raises(ValueError, match="missing required field"):
            validate_answer_structure(answer)
    
    def test_empty_options_raises(self):
        """Test that empty options raises ValueError."""
        answer = {
            "questionId": "q1",
            "selectedOptions": []
        }
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_answer_structure(answer)


class TestValidateUserId:
    """Test user ID validation."""
    
    def test_valid_user_id(self):
        """Test validation of valid user ID."""
        assert validate_user_id("user123")
        assert validate_user_id("user-123")
        assert validate_user_id("user_123")
    
    def test_empty_user_id_raises(self):
        """Test that empty user ID raises ValueError."""
        with pytest.raises(ValueError, match="non-empty string"):
            validate_user_id("")
    
    def test_too_long_user_id_raises(self):
        """Test that user ID exceeding 128 chars raises ValueError."""
        with pytest.raises(ValueError, match="cannot exceed 128"):
            validate_user_id("x" * 129)
    
    def test_invalid_characters_raises(self):
        """Test that invalid characters raise ValueError."""
        with pytest.raises(ValueError, match="alphanumeric"):
            validate_user_id("user@123")


class TestValidateSessionId:
    """Test session ID validation."""
    
    def test_valid_session_id(self):
        """Test validation of valid session ID (UUID)."""
        session_id = str(uuid.uuid4())
        assert validate_session_id(session_id)
    
    def test_invalid_session_id_raises(self):
        """Test that invalid session ID raises ValueError."""
        with pytest.raises(ValueError, match="sessionId"):
            validate_session_id("not-a-uuid")


class TestValidateTasteDNA:
    """Test taste DNA validation."""
    
    @pytest.fixture
    def valid_dna(self):
        """Valid taste DNA structure."""
        return {
            "archetype": "The Curator",
            "description": "Refined taste profile",
            "traits": [
                {
                    "name": "Aesthetic Sensitivity",
                    "score": 8.5,
                    "description": "High appreciation for beauty"
                }
            ],
            "categories": {
                "visual": ["minimalist", "contemporary"],
                "mood": ["reflective"]
            }
        }
    
    def test_valid_dna(self, valid_dna):
        """Test validation of valid taste DNA."""
        assert validate_taste_dna(valid_dna)
    
    def test_missing_field_raises(self, valid_dna):
        """Test that missing field raises ValueError."""
        invalid = valid_dna.copy()
        del invalid["archetype"]
        
        with pytest.raises(ValueError, match="missing required field"):
            validate_taste_dna(invalid)
    
    def test_invalid_trait_score_raises(self, valid_dna):
        """Test that invalid trait score raises ValueError."""
        invalid = valid_dna.copy()
        invalid["traits"][0]["score"] = 15  # Out of bounds
        
        with pytest.raises(ValueError, match="between 0 and 10"):
            validate_taste_dna(invalid)
    
    def test_missing_trait_field_raises(self, valid_dna):
        """Test that missing trait field raises ValueError."""
        invalid = valid_dna.copy()
        del invalid["traits"][0]["score"]
        
        with pytest.raises(ValueError, match="must have 'name' and 'score'"):
            validate_taste_dna(invalid)


class TestValidateGrowthPath:
    """Test growth path validation."""
    
    @pytest.fixture
    def valid_path(self):
        """Valid growth path structure."""
        return {
            "absorb": [
                {"title": "Rec 1", "description": "Desc 1"},
                {"title": "Rec 2", "description": "Desc 2"},
                {"title": "Rec 3", "description": "Desc 3"}
            ],
            "create": [
                {"title": "Rec 4", "description": "Desc 4"},
                {"title": "Rec 5", "description": "Desc 5"},
                {"title": "Rec 6", "description": "Desc 6"}
            ],
            "reflect": [
                {"title": "Rec 7", "description": "Desc 7"},
                {"title": "Rec 8", "description": "Desc 8"},
                {"title": "Rec 9", "description": "Desc 9"}
            ]
        }
    
    def test_valid_path(self, valid_path):
        """Test validation of valid growth path."""
        assert validate_growth_path(valid_path)
    
    def test_missing_category_raises(self, valid_path):
        """Test that missing category raises ValueError."""
        invalid = valid_path.copy()
        del invalid["absorb"]
        
        with pytest.raises(ValueError, match="missing required category"):
            validate_growth_path(invalid)
    
    def test_too_few_recommendations_raises(self, valid_path):
        """Test that too few recommendations raises ValueError."""
        invalid = valid_path.copy()
        invalid["absorb"] = [{"title": "Rec", "description": "Desc"}]
        
        with pytest.raises(ValueError, match="3-5 recommendations"):
            validate_growth_path(invalid)
    
    def test_too_many_recommendations_raises(self, valid_path):
        """Test that too many recommendations raises ValueError."""
        invalid = valid_path.copy()
        invalid["absorb"] = [
            {"title": f"Rec {i}", "description": f"Desc {i}"}
            for i in range(10)
        ]
        
        with pytest.raises(ValueError, match="3-5 recommendations"):
            validate_growth_path(invalid)
    
    def test_missing_recommendation_field_raises(self, valid_path):
        """Test that missing recommendation field raises ValueError."""
        invalid = valid_path.copy()
        del invalid["absorb"][0]["title"]
        
        with pytest.raises(ValueError, match="must have 'title' and 'description'"):
            validate_growth_path(invalid)
