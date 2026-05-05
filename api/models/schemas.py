# api/models/schemas.py
from pydantic import BaseModel
from typing import Optional, List

# ===== REQUEST MODELS =====
class QuestionRequest(BaseModel):
    question: str
    k: Optional[int] = 5

class DocumentRequest(BaseModel):
    doc_type: str
    party1: str
    party2: str
    terms: str
    extra_details: Optional[str] = ""

class ResearchRequest(BaseModel):
    topic: str

# ===== RESPONSE MODELS =====
class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    status: str

class DocumentResponse(BaseModel):
    doc_type: str
    document: str
    saved_to: str
    status: str

class ResearchResponse(BaseModel):
    topic: str
    research: str
    status: str

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str
    total_vectors: int
    total_chunks: int