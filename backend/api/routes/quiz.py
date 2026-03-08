"""
Quiz API Routes

Handles adaptive quiz flow:
- Section 1: Start quiz and get foundational questions
- Section 2: Generate adaptive questions based on Section 1
- Complete: Generate embedding and taste DNA
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/quiz", tags=["quiz"])


# Request/Response Models
class StartSection1Request(BaseModel):
    userId: Optional[str] = None


class StartSection1Response(BaseModel):
    sessionId: str
    questions: List[Dict[str, Any]]


class GenerateSection2Request(BaseModel):
    sessionId: str
    section1Answers: List[Dict[str, Any]]


class GenerateSection2Response(BaseModel):
    questions: List[Dict[str, Any]]


class CompleteQuizRequest(BaseModel):
    sessionId: str
    userId: str
    allAnswers: Dict[str, List[Dict[str, Any]]]


class CompleteQuizResponse(BaseModel):
    embeddingId: str
    tasteDNA: Dict[str, Any]


@router.post("/section1/start", response_model=StartSection1Response)
async def start_section1(request: StartSection1Request):
    """
    Start Section 1 of the adaptive quiz.
    
    Returns:
        - sessionId: Unique session identifier
        - questions: List of 5 foundational questions
    """
    try:
        logger.info("Starting Section 1")
        
        # Import handler
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.handlers.generate_section1 import generate_section1
        
        # Call real handler
        result = generate_section1()
        
        return StartSection1Response(
            sessionId=result["sessionId"],
            questions=result["questions"]
        )
        
    except Exception as e:
        logger.error(f"Error starting Section 1: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/section2/generate", response_model=GenerateSection2Response)
async def generate_section2(request: GenerateSection2Request):
    """
    Generate adaptive Section 2 questions based on Section 1 answers.
    
    Returns:
        - questions: List of 5 adaptive questions
    """
    try:
        logger.info(f"Generating Section 2 for session {request.sessionId}")
        
        # Import handler
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.handlers.generate_section2 import generate_section2 as gen_s2
        
        # Call real handler
        result = gen_s2(request.sessionId, request.section1Answers)
        
        return GenerateSection2Response(questions=result["questions"])
        
    except Exception as e:
        logger.error(f"Error generating Section 2: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete", response_model=CompleteQuizResponse)
async def complete_quiz(request: CompleteQuizRequest):
    """
    Complete quiz and generate taste profile.
    
    Returns:
        - embeddingId: ID of generated embedding
        - tasteDNA: Taste DNA profile with archetype and traits
    """
    try:
        logger.info(f"Completing quiz for session {request.sessionId}, user {request.userId}")
        
        # Import handlers
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.handlers.generate_embedding import generate_embedding
        from src.handlers.generate_dna import generate_dna
        
        # Extract answers
        section1_answers = request.allAnswers.get("section1", [])
        section2_answers = request.allAnswers.get("section2", [])
        
        # Generate embedding
        embedding_result = generate_embedding(
            request.userId,
            section1_answers,
            section2_answers
        )
        
        # Generate DNA
        dna_result = generate_dna(
            request.userId,
            section1_answers,
            section2_answers
        )
        
        return CompleteQuizResponse(
            embeddingId=embedding_result["embeddingId"],
            tasteDNA=dna_result
        )
        
    except Exception as e:
        logger.error(f"Error completing quiz: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
