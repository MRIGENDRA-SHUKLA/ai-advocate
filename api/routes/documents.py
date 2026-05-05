# api/routes/documents.py
from fastapi import APIRouter, HTTPException
from models.schemas import DocumentRequest, DocumentResponse
from agents.orchestrator import Orchestrator

# Create router
router = APIRouter()

# Initialize orchestrator once
orchestrator = Orchestrator()

@router.post("/generate-doc", response_model=DocumentResponse)
def generate_document(req: DocumentRequest):
    """
    Generate a professional legal document.
    
    The system will:
    1. Take document type and party details
    2. Generate complete professional document
    3. Save to outputs/ folder
    4. Return full document text
    
    Supported documents:
    - Rental Agreement
    - Non Disclosure Agreement (NDA)
    - Employment Contract
    - Partnership Deed
    - Service Agreement
    - Loan Agreement
    - Sale Agreement
    - Will and Testament
    - Power of Attorney
    - Affidavit
    
    Example request:
    {
        "doc_type": "Rental Agreement",
        "party1": "Ramesh Kumar (Landlord), Mumbai",
        "party2": "Suresh Singh (Tenant), Mumbai",
        "terms": "Monthly rent 15000, 11 months",
        "extra_details": "2 month security deposit"
    }
    """
    try:
        print(f"\n📥 /generate-doc request received")
        print(f"   Doc type: {req.doc_type}")
        print(f"   Party 1 : {req.party1[:40]}...")
        print(f"   Party 2 : {req.party2[:40]}...")
        
        # Route through orchestrator
        result = orchestrator.handle_document(
            doc_type     = req.doc_type,
            party1       = req.party1,
            party2       = req.party2,
            terms        = req.terms,
            extra_details= req.extra_details
        )
        
        print(f"✅ /generate-doc response sent!")
        print(f"   Document length: {result['length']} chars")
        
        return DocumentResponse(
            doc_type = req.doc_type,
            document = result['document'],
            saved_to = result['saved_to'],
            status   = result['status']
        )
    
    except Exception as e:
        print(f"❌ /generate-doc error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating document: {str(e)}"
        )

@router.get("/supported-docs")
def get_supported_documents():
    """
    Get list of all supported document types.
    
    Returns list of documents that can be generated
    by the Document Agent.
    """
    try:
        supported = orchestrator.document_agent\
            .get_supported_documents()
        
        return {
            "supported_documents": supported,
            "total"              : len(supported),
            "status"             : "success"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )