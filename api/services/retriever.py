# api/services/retriever.py
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ===== LOAD FAISS INDEX AND METADATA =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAISS_PATH = os.path.join(BASE_DIR, 'vector_store', 'legal_index.faiss')
METADATA_PATH = os.path.join(BASE_DIR, 'vector_store', 'metadata.json')

print("⏳ Loading FAISS index...")
index = faiss.read_index(FAISS_PATH)
print(f"✅ FAISS loaded: {index.ntotal} vectors")

print("⏳ Loading metadata...")
with open(METADATA_PATH, 'r', encoding='utf-8') as f:
    chunks = json.load(f)
print(f"✅ Metadata loaded: {len(chunks)} chunks")

print("⏳ Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Embedding model loaded!")

# ===== RETRIEVAL FUNCTIONS =====
def retrieve(query: str, k: int = 5) -> list:
    """
    Search FAISS for most relevant law sections.
    
    Args:
        query: Legal question or search text
        k: Number of results to return
    
    Returns:
        list: Top k relevant law sections with metadata
    """
    # Convert query to vector
    query_vector = embedding_model.encode(
        [query]).astype('float32')
    
    # Search FAISS
    distances, indices = index.search(query_vector, k=k)
    
    # Build results with metadata
    results = []
    for i, idx in enumerate(indices[0]):
        chunk = chunks[idx]
        results.append({
            'rank'    : i + 1,
            'distance': round(float(distances[0][i]), 4),
            'act'     : chunk['act_title'],
            'section' : chunk['section_id'],
            'heading' : chunk['section_heading'],
            'text'    : chunk['text'],
            'chapter' : chunk.get('chapter_name', ''),
            'date'    : chunk.get('enactment_date', '')
        })
    return results

def retrieve_with_context(query: str, k: int = 5) -> tuple:
    """
    Retrieve sections and build context string for LLM.
    
    Args:
        query: Legal question
        k: Number of sections to retrieve
    
    Returns:
        tuple: (context_string, sources_list)
    """
    results = retrieve(query, k=k)
    
    # Build context string
    context = ""
    sources = []
    
    for r in results:
        context += f"\nAct: {r['act']}\n"
        context += f"Section: {r['section']} - {r['heading']}\n"
        context += f"Text: {r['text']}\n"
        context += "-" * 40 + "\n"
        sources.append(
            f"{r['act']} — {r['section']} {r['heading']}"
        )
    
    return context, sources

def get_stats() -> dict:
    """Return statistics about the vector store"""
    return {
        'total_vectors'  : index.ntotal,
        'total_chunks'   : len(chunks),
        'embedding_model': 'all-MiniLM-L6-v2',
        'dimensions'     : 384,
        'index_type'     : 'IndexFlatL2'
    }