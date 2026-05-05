# api/routes/ask.py
from fastapi import APIRouter, HTTPException
from models.schemas import QuestionRequest, QuestionResponse
from agents.orchestrator import Orchestrator

# Create router
router = APIRouter()

# Initialize orchestrator once
orchestrator = Orchestrator()

@router.post("/ask", response_model=QuestionResponse)
def ask_question(req: QuestionRequest):
    """
    Ask a legal question and get an answer.
    
    The system will:
    1. Search 56,617 Indian law sections
    2. Find most relevant sections
    3. Generate answer using Groq LLaMA
    4. Return answer with source citations
    
    Example request:
    {
        "question": "What is the punishment for murder?",
        "k": 5
    }
    
    Example response:
    {
        "question": "What is the punishment for murder?",
        "answer": "Under Section 302 of IPC...",
        "sources": ["THE INDIAN PENAL CODE — Section 302"],
        "status": "success"
    }
    """
    try:
        print(f"\n📥 /ask request received")
        print(f"   Question: {req.question[:60]}...")
        print(f"   K       : {req.k}")
        
        # Route through orchestrator
        result = orchestrator.handle_question(
            question=req.question,
            k=req.k
        )
        
        print(f"✅ /ask response sent!")
        
        return QuestionResponse(
            question=req.question,
            answer=result['answer'],
            sources=result.get('sources', []),
            status=result['status']
        )
    
    except Exception as e:
        print(f"❌ /ask error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )

@router.post("/search")
def search_sections(req: QuestionRequest):
    """
    Search for relevant law sections without generating answer.
    Returns raw FAISS search results.
    
    Useful when you want to see which law sections
    are most relevant to a query.
    
    Example request:
    {
        "question": "income tax penalty",
        "k": 5
    }
    """
    try:
        print(f"\n📥 /search request received")
        print(f"   Query: {req.question[:60]}...")
        
        # Search only — no answer generation
        result = orchestrator.retrieval_agent.search_only(
            query=req.question,
            k=req.k
        )
        
        print(f"✅ /search response sent!")
        
        return {
            "query"  : req.question,
            "results": result['results'],
            "count"  : result['count'],
            "status" : result['status']
        }
    
    except Exception as e:
        print(f"❌ /search error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching: {str(e)}"
        )