# api/routes/research.py
from fastapi import APIRouter, HTTPException
from models.schemas import ResearchRequest, ResearchResponse
from agents.orchestrator import Orchestrator

# Create router
router = APIRouter()

# Initialize orchestrator once
orchestrator = Orchestrator()

@router.post("/research", response_model=ResearchResponse)
def research_topic(req: ResearchRequest):
    """
    Research any Indian legal topic comprehensively.
    
    The system will:
    1. Take legal topic from user
    2. Generate comprehensive research using Groq
    3. Cover relevant Acts, Sections, provisions
    4. Save research to outputs/ folder
    5. Return complete research summary
    
    Example request:
    {
        "topic": "Rights of an arrested person in India"
    }
    
    Example response:
    {
        "topic": "Rights of an arrested person in India",
        "research": "Under Article 22 of Constitution...",
        "status": "success"
    }
    
    Research areas covered:
    - Criminal Law (IPC, CrPC)
    - Civil Law (CPC)
    - Corporate Law (Companies Act)
    - Tax Law (Income Tax, GST)
    - Labour Law
    - Constitutional Law
    - Property Law
    - Family Law
    - Consumer Protection Law
    - Cyber Law (IT Act)
    """
    try:
        print(f"\n📥 /research request received")
        print(f"   Topic: {req.topic[:60]}...")
        
        # Route through orchestrator
        result = orchestrator.handle_research(
            topic=req.topic
        )
        
        print(f"✅ /research response sent!")
        print(f"   Research length: {result['length']} chars")
        
        return ResearchResponse(
            topic    = req.topic,
            research = result['research'],
            status   = result['status']
        )
    
    except Exception as e:
        print(f"❌ /research error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error researching topic: {str(e)}"
        )

@router.get("/research-areas")
def get_research_areas():
    """
    Get list of all research areas covered.
    
    Returns list of legal areas that the
    Research Agent can provide information on.
    """
    try:
        areas = orchestrator.research_agent\
            .get_research_areas()
        
        return {
            "research_areas": areas,
            "total"         : len(areas),
            "status"        : "success"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )