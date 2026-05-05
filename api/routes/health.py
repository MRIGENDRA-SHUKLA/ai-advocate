# api/routes/health.py
from fastapi import APIRouter
from services.retriever import get_stats

# Create router
router = APIRouter()

@router.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns system status and statistics.
    
    Use this to verify:
    - API is running
    - FAISS is loaded
    - How many vectors are in the database
    """
    try:
        # Get FAISS stats
        stats = get_stats()
        
        return {
            "status"        : "running",
            "message"       : "AI Advocate API is live!",
            "version"       : "1.0.0",
            "total_vectors" : stats['total_vectors'],
            "total_chunks"  : stats['total_chunks'],
            "embedding_model": stats['embedding_model'],
            "index_type"    : stats['index_type']
        }
    
    except Exception as e:
        return {
            "status" : "error",
            "message": f"System error: {str(e)}",
            "version": "1.0.0"
        }

@router.get("/stats")
def get_system_stats():
    """
    Detailed system statistics endpoint.
    Returns complete information about the system.
    """
    try:
        from agents.orchestrator import Orchestrator
        
        # Get FAISS stats
        faiss_stats = get_stats()
        
        # Get agent info
        orchestrator = Orchestrator()
        agent_info = orchestrator.get_system_info()
        
        return {
            "status"    : "operational",
            "version"   : "1.0.0",
            "faiss"     : faiss_stats,
            "agents"    : agent_info,
            "endpoints" : [
                "GET  /health",
                "GET  /stats",
                "POST /ask",
                "POST /generate-doc",
                "POST /research"
            ]
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error" : str(e)
        }