"""
Integration test for complete quiz flow.

Tests the end-to-end quiz experience:
1. Start Section 1
2. Submit Section 1 answers
3. Generate Section 2
4. Submit Section 2 answers
5. Complete quiz and receive taste DNA
"""

import pytest
import requests
import time
from typing import Dict, List


# Configuration
API_BASE_URL = "http://localhost:8000"
TIMEOUT = 30


class TestQuizFlow:
    """Integration tests for complete quiz flow."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client for testing."""
        return requests.Session()
    
    def test_complete_quiz_flow(self, api_client):
        """
        Test complete quiz flow from start to finish.
        
        This test verifies:
        - Section 1 generation
        - Session management
        - Section 2 adaptive generation
        - Quiz completion with embedding and DNA generation
        """
        # Step 1: Start Section 1
        response = api_client.post(
            f"{API_BASE_URL}/quiz/section1/start",
            json={"userId": "test-user-integration"},
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200, f"Section 1 start failed: {response.text}"
        
        section1_data = response.json()
        assert "sessionId" in section1_data
        assert "questions" in section1_data
        assert len(section1_data["questions"]) == 5
        
        session_id = section1_data["sessionId"]
        section1_questions = section1_data["questions"]
        
        # Verify question structure
        for question in section1_questions:
            assert "id" in question
            assert "title" in question
            assert "category" in question
            assert "options" in question
            assert "multiSelect" in question
            assert len(question["options"]) > 0
        
        # Step 2: Submit Section 1 answers
        section1_answers = [
            {
                "questionId": q["id"],
                "selectedOptions": [q["options"][0]]  # Select first option
            }
            for q in section1_questions
        ]
        
        # Step 3: Generate Section 2
        response = api_client.post(
            f"{API_BASE_URL}/quiz/section2/generate",
            json={
                "sessionId": session_id,
                "section1Answers": section1_answers
            },
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200, f"Section 2 generation failed: {response.text}"
        
        section2_data = response.json()
        assert "questions" in section2_data
        assert len(section2_data["questions"]) == 5
        
        section2_questions = section2_data["questions"]
        
        # Step 4: Submit Section 2 answers
        section2_answers = [
            {
                "questionId": q["id"],
                "selectedOptions": [q["options"][0]]
            }
            for q in section2_questions
        ]
        
        # Step 5: Complete quiz
        response = api_client.post(
            f"{API_BASE_URL}/quiz/complete",
            json={
                "sessionId": session_id,
                "userId": "test-user-integration",
                "allAnswers": {
                    "section1": section1_answers,
                    "section2": section2_answers
                }
            },
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200, f"Quiz completion failed: {response.text}"
        
        completion_data = response.json()
        assert "embeddingId" in completion_data
        assert "tasteDNA" in completion_data
        
        # Verify taste DNA structure
        taste_dna = completion_data["tasteDNA"]
        assert "archetype" in taste_dna
        assert "traits" in taste_dna
        assert "categories" in taste_dna
        assert "description" in taste_dna
        
        # Verify traits structure
        assert len(taste_dna["traits"]) > 0
        for trait in taste_dna["traits"]:
            assert "name" in trait
            assert "score" in trait
            assert "description" in trait
            assert 0 <= trait["score"] <= 10
        
        # Verify categories structure
        assert len(taste_dna["categories"]) > 0
        for category in taste_dna["categories"]:
            assert "category" in category
            assert "preferences" in category
            assert "intensity" in category
            assert len(category["preferences"]) > 0
    
    def test_session_expiration(self, api_client):
        """
        Test that expired sessions are rejected.
        
        Note: This test requires a session that has expired (1 hour old).
        In a real test, you might mock the time or use a shorter TTL.
        """
        # Use an expired or invalid session ID
        expired_session_id = "expired-session-123"
        
        response = api_client.post(
            f"{API_BASE_URL}/quiz/section2/generate",
            json={
                "sessionId": expired_session_id,
                "section1Answers": [
                    {"questionId": "q1", "selectedOptions": ["Option A"]}
                ] * 5
            },
            timeout=TIMEOUT
        )
        
        assert response.status_code == 404
        error_data = response.json()
        assert "expired" in error_data["message"].lower() or "not found" in error_data["message"].lower()
    
    def test_invalid_answers_rejected(self, api_client):
        """Test that invalid quiz answers are rejected with validation errors."""
        # Start Section 1 to get valid session
        response = api_client.post(
            f"{API_BASE_URL}/quiz/section1/start",
            json={},
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        session_id = response.json()["sessionId"]
        
        # Try to submit invalid answers (wrong count)
        response = api_client.post(
            f"{API_BASE_URL}/quiz/section2/generate",
            json={
                "sessionId": session_id,
                "section1Answers": [
                    {"questionId": "q1", "selectedOptions": ["Option A"]}
                ]  # Only 1 answer instead of 5
            },
            timeout=TIMEOUT
        )
        
        assert response.status_code == 400
        error_data = response.json()
        assert "message" in error_data


class TestMatchingFlow:
    """Integration tests for taste matching flow."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client for testing."""
        return requests.Session()
    
    @pytest.mark.skip(reason="Requires multiple users with embeddings")
    def test_find_matches(self, api_client):
        """
        Test finding taste matches for a user.
        
        Prerequisites:
        - Multiple users with completed quizzes
        - Embedding vectors stored in database
        """
        user_id = "test-user-123"
        
        response = api_client.get(
            f"{API_BASE_URL}/profile/matches/{user_id}",
            params={"limit": 10},
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        
        matches_data = response.json()
        assert "matches" in matches_data
        
        # Verify match structure
        for match in matches_data["matches"]:
            assert "userId" in match
            assert "username" in match
            assert "similarity" in match
            assert "sharedTraits" in match
            assert "archetype" in match
            
            # Verify similarity bounds
            assert 0.7 <= match["similarity"] <= 1.0
            
            # Verify user is not matched with themselves
            assert match["userId"] != user_id


class TestGrowthPathFlow:
    """Integration tests for growth path generation."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client for testing."""
        return requests.Session()
    
    @pytest.mark.skip(reason="Requires user with completed quiz")
    def test_generate_growth_path(self, api_client):
        """
        Test growth path generation for a user.
        
        Prerequisites:
        - User with completed quiz and taste DNA
        """
        user_id = "test-user-123"
        
        response = api_client.get(
            f"{API_BASE_URL}/profile/path/{user_id}",
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        
        path_data = response.json()
        assert "path" in path_data
        
        path = path_data["path"]
        assert "absorb" in path
        assert "create" in path
        assert "reflect" in path
        assert "generatedAt" in path
        
        # Verify each category has recommendations
        for category in ["absorb", "create", "reflect"]:
            recommendations = path[category]
            assert 3 <= len(recommendations) <= 5
            
            for rec in recommendations:
                assert "id" in rec
                assert "title" in rec
                assert "description" in rec
                assert "category" in rec
                assert "estimatedTime" in rec
                assert "difficulty" in rec
                assert rec["difficulty"] in ["beginner", "intermediate", "advanced"]
