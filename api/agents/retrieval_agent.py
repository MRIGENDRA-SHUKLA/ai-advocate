# api/agents/retrieval_agent.py
from services.generator import generate_legal_answer
from services.retriever import retrieve

class RetrievalAgent:
    """
    Specialist agent for legal question answering.
    Searches FAISS and generates answers using Groq.
    
    Called when user asks a legal question.
    Example: "What is the punishment for murder?"
    """
    
    def __init__(self):
        self.name = "Retrieval Agent"
        self.description = "Searches Indian law sections and answers legal questions"
    
    def run(self, question: str, k: int = 5) -> dict:
        """
        Answer a legal question using RAG pipeline.
        
        Args:
            question: Legal question from user
            k: Number of law sections to retrieve
        
        Returns:
            dict: answer, sources, agent name, status
        """
        print(f"🔍 Retrieval Agent activated!")
        print(f"   Question: {question[:60]}...")
        
        try:
            # Generate answer using RAG pipeline
            answer, sources = generate_legal_answer(
                question, k=k)
            
            print(f"✅ Answer generated!")
            print(f"   Sources: {len(sources)} sections found")
            
            return {
                'agent'   : self.name,
                'question': question,
                'answer'  : answer,
                'sources' : sources,
                'status'  : 'success'
            }
        
        except Exception as e:
            print(f"❌ Retrieval Agent error: {str(e)}")
            return {
                'agent'   : self.name,
                'question': question,
                'answer'  : f"Error: {str(e)}",
                'sources' : [],
                'status'  : 'error'
            }
    
    def search_only(self, query: str, k: int = 5) -> dict:
        """
        Only search FAISS without generating answer.
        Useful for getting raw law sections.
        
        Args:
            query: Search query
            k: Number of results
        
        Returns:
            dict: raw search results
        """
        print(f"🔍 Search only mode: {query[:60]}...")
        
        try:
            results = retrieve(query, k=k)
            return {
                'agent'  : self.name,
                'query'  : query,
                'results': results,
                'count'  : len(results),
                'status' : 'success'
            }
        
        except Exception as e:
            return {
                'agent'  : self.name,
                'query'  : query,
                'results': [],
                'count'  : 0,
                'status' : 'error',
                'error'  : str(e)
            }