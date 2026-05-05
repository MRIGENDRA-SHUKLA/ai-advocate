# api/agents/document_agent.py
import os
from services.generator import generate_legal_document

class DocumentAgent:
    """
    Specialist agent for legal document generation.
    Drafts professional legal documents using Groq.
    
    Called when user wants to CREATE a document.
    Example: "Draft a rental agreement"
    """
    
    def __init__(self):
        self.name = "Document Agent"
        self.description = "Drafts professional legal documents under Indian law"
        self.supported_documents = [
            "Rental Agreement",
            "Non Disclosure Agreement",
            "Employment Contract",
            "Partnership Deed",
            "Service Agreement",
            "Loan Agreement",
            "Sale Agreement",
            "Will and Testament",
            "Power of Attorney",
            "Affidavit"
        ]
    
    def run(
        self,
        doc_type: str,
        party1: str,
        party2: str,
        terms: str,
        extra_details: str = ""
    ) -> dict:
        """
        Generate a professional legal document.
        
        Args:
            doc_type: Type of document
            party1: First party details
            party2: Second party details
            terms: Key terms and conditions
            extra_details: Additional details
        
        Returns:
            dict: document, filename, agent name, status
        """
        print(f"📝 Document Agent activated!")
        print(f"   Document type : {doc_type}")
        print(f"   Party 1       : {party1[:40]}...")
        print(f"   Party 2       : {party2[:40]}...")
        
        try:
            # Generate document
            document, filename = generate_legal_document(
                doc_type=doc_type,
                party1=party1,
                party2=party2,
                terms=terms,
                extra_details=extra_details
            )
            
            print(f"✅ Document generated!")
            print(f"   Length  : {len(document)} characters")
            print(f"   Saved to: {filename}")
            
            return {
                'agent'   : self.name,
                'doc_type': doc_type,
                'document': document,
                'saved_to': filename,
                'length'  : len(document),
                'status'  : 'success'
            }
        
        except Exception as e:
            print(f"❌ Document Agent error: {str(e)}")
            return {
                'agent'   : self.name,
                'doc_type': doc_type,
                'document': f"Error generating document: {str(e)}",
                'saved_to': '',
                'length'  : 0,
                'status'  : 'error'
            }
    
    def get_supported_documents(self) -> list:
        """Return list of supported document types"""
        return self.supported_documents
    
    def is_supported(self, doc_type: str) -> bool:
        """
        Check if document type is supported.
        
        Args:
            doc_type: Document type to check
        
        Returns:
            bool: True if supported
        """
        return any(
            doc.lower() in doc_type.lower()
            for doc in self.supported_documents
        )