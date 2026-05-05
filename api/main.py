# api/main.py
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add api/ folder to Python path
# This allows imports like "from services.groq_client import..."
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all routers
from routes.health import router as health_router
from routes.ask import router as ask_router
from routes.documents import router as documents_router
from routes.research import router as research_router

# ===== CREATE FASTAPI APP =====
app = FastAPI(
    title="AI Advocate API",
    description="""
## AI Advocate — Multi-Agent RAG Legal Assistant

A production-ready API that answers Indian legal questions,
drafts legal documents, and performs legal research using
56,617 chunks from 855 unique Indian Acts.

### Features:
- **Legal Q&A** → Ask any Indian legal question
- **Document Generation** → Draft professional legal documents
- **Legal Research** → Comprehensive research on legal topics
- **FAISS Search** → Direct vector database search

### Tech Stack:
- **FAISS** → Vector database with 56,617 legal sections
- **Groq LLaMA 3.3 70B** → Answer generation
- **Sentence Transformers** → Text embeddings
- **FastAPI** → REST API framework

### Data:
- 855 unique Indian Acts
- 30,444 original sections
- 56,617 chunks after processing
    """,
    version="1.0.0",
    contact={
        "name" : "AI Advocate",
        "email": "contact@ai-advocate.com"
    }
)

# ===== ADD CORS MIDDLEWARE =====
# Allows frontend apps to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],     # Allow all methods
    allow_headers=["*"],     # Allow all headers
)

# ===== REGISTER ALL ROUTERS =====
app.include_router(health_router,    tags=["Health"])
app.include_router(ask_router,       tags=["Legal Q&A"])
app.include_router(documents_router, tags=["Documents"])
app.include_router(research_router,  tags=["Research"])

# ===== ROOT ENDPOINT =====
@app.get("/")
def root():
    """
    Root endpoint — welcome message.
    Visit /docs for interactive API documentation.
    """
    return {
        "message"    : "Welcome to AI Advocate API!",
        "version"    : "1.0.0",
        "docs"       : "/docs",
        "health"     : "/health",
        "endpoints"  : {
            "legal_qa"  : "POST /ask",
            "search"    : "POST /search",
            "documents" : "POST /generate-doc",
            "research"  : "POST /research",
            "health"    : "GET /health",
            "stats"     : "GET /stats"
        }
    }

# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup_event():
    """
    Runs when API starts.
    Logs startup message.
    """
    print()
    print("=" * 60)
    print("🚀 AI Advocate API Starting...")
    print("=" * 60)
    print("✅ FAISS index loading...")
    print("✅ Embedding model loading...")
    print("✅ Groq client connecting...")
    print("✅ All agents initializing...")
    print()
    print("📚 Swagger UI : http://127.0.0.1:8000/docs")
    print("🔍 Health     : http://127.0.0.1:8000/health")
    print("=" * 60)
    print()

# ===== SHUTDOWN EVENT =====
@app.on_event("shutdown")
async def shutdown_event():
    """Runs when API stops"""
    print()
    print("=" * 60)
    print("👋 AI Advocate API Shutting down...")
    print("=" * 60)

# ===== RUN SERVER =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True      # Auto restart on code changes
    )