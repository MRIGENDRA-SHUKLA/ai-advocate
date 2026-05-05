# api/services/generator.py
from services.groq_client import call_groq
from services.retriever import retrieve_with_context

def generate_legal_answer(question: str, k: int = 5) -> tuple:
    """
    Full RAG pipeline — retrieve + generate answer.
    
    Args:
        question: Legal question from user
        k: Number of sections to retrieve
    
    Returns:
        tuple: (answer, sources)
    """
    # Step 1 — Retrieve relevant law sections
    context, sources = retrieve_with_context(question, k=k)
    
    # Step 2 — Build prompt
    prompt = f"""You are an expert Indian legal assistant.
Answer this legal question based on the law sections below.
Be specific and cite exact Act and Section numbers.
Use simple clear language anyone can understand.

LAW SECTIONS:
{context}

QUESTION: {question}

Provide a clear, accurate answer with citations."""

    system_prompt = """You are an expert Indian legal assistant
with deep knowledge of all Indian Acts and Sections.
Always cite the exact Act name and Section number.
Be accurate, clear and helpful."""

    # Step 3 — Generate answer with Groq
    answer = call_groq(prompt, system_prompt)
    
    return answer, sources


def generate_legal_document(
    doc_type: str,
    party1: str,
    party2: str,
    terms: str,
    extra_details: str = ""
) -> tuple:
    """
    Generate a professional legal document.
    
    Args:
        doc_type: Type of document (Rental Agreement, NDA etc)
        party1: First party details
        party2: Second party details
        terms: Key terms and conditions
        extra_details: Additional details
    
    Returns:
        tuple: (document_text, filename)
    """
    # Build prompt
    prompt = f"""Draft a complete professional {doc_type}
under Indian law with these details:

Party 1       : {party1}
Party 2       : {party2}
Key Terms     : {terms}
Extra Details : {extra_details}

Include these sections:
1. Document Title and Date
2. Parties Section with full details
3. Recitals (WHEREAS clauses)
4. Terms and Conditions (minimum 8 clauses)
5. Payment Terms
6. Duration and Renewal
7. Termination Clause with notice period
8. Dispute Resolution and Arbitration
9. Governing Law (mention Indian Acts)
10. Force Majeure
11. Signature Section with witnesses

Make it legally sound and professional."""

    system_prompt = """You are an expert Indian legal
document drafter with 20 years of experience.
Always create complete, professional documents
that are legally sound under Indian law."""

    # Generate document
    document = call_groq(prompt, system_prompt)

    # Create filename
    filename = f"outputs/{doc_type.replace(' ', '_')}.txt"

    # Save document
    try:
        import os
        os.makedirs('outputs', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Document Type: {doc_type}\n")
            f.write(f"Party 1: {party1}\n")
            f.write(f"Party 2: {party2}\n")
            f.write("=" * 60 + "\n\n")
            f.write(document)
    except Exception as e:
        print(f"⚠️ Could not save document: {e}")

    return document, filename


def generate_legal_research(topic: str) -> str:
    """
    Research a legal topic comprehensively.
    
    Args:
        topic: Legal topic to research
    
    Returns:
        str: Comprehensive research summary
    """
    prompt = f"""Research this Indian legal topic
comprehensively:

Topic: {topic}

Include:
1. Overview under Indian law
2. Relevant Acts and Sections
3. Key legal provisions
4. Rights and obligations
5. Penalties and consequences
6. Recent developments
7. Practical implications
8. Important case references

Be specific, accurate and cite Indian laws."""

    system_prompt = """You are an expert Indian legal
researcher with comprehensive knowledge of all
Indian laws, Acts, and legal precedents."""

    return call_groq(prompt, system_prompt)