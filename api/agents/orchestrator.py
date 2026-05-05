# api/agents/orchestrator.py
from agents.retrieval_agent import RetrievalAgent
from agents.document_agent import DocumentAgent
from agents.research_agent import ResearchAgent

class Orchestrator:
    """
    BOSS Agent — reads user input and routes to
    correct specialist agent automatically.
    
    Routing Rules:
    - draft/contract/agreement/nda → Document Agent
    - research/explain/what is/tell me → Research Agent
    - everything else → Retrieval Agent
    """
    
    def __init__(self):
        self.name = "Orchestrator"
        self.description = "Routes requests to correct specialist agent"
        
        # Initialize all agents
        self.retrieval_agent = RetrievalAgent()
        self.document_agent  = DocumentAgent()
        self.research_agent  = ResearchAgent()
        
        # Keywords for routing
        self.document_keywords = [
            'draft', 'create', 'write', 'generate',
            'agreement', 'contract', 'nda', 'deed',
            'document', 'lease', 'rental', 'employment',
            'partnership', 'service', 'affidavit',
            'will', 'power of attorney', 'format'
        ]
        
        self.research_keywords = [
            'research', 'explain', 'what is', 'tell me',
            'describe', 'overview', 'summary', 'about',
            'how does', 'define', 'meaning', 'elaborate',
            'details about', 'information on', 'guide'
        ]
        
        print("✅ Orchestrator initialized!")
        print(f"   → {self.retrieval_agent.name}")
        print(f"   → {self.document_agent.name}")
        print(f"   → {self.research_agent.name}")
    
    def route(self, user_input: str) -> str:
        """
        Determine which agent should handle the request.
        
        Args:
            user_input: User's query or request
        
        Returns:
            str: 'document', 'research', or 'retrieval'
        """
        input_lower = user_input.lower()
        
        # Check document keywords first
        if any(kw in input_lower
               for kw in self.document_keywords):
            return 'document'
        
        # Check research keywords
        elif any(kw in input_lower
                 for kw in self.research_keywords):
            return 'research'
        
        # Default to retrieval
        else:
            return 'retrieval'
    
    def handle_question(
        self,
        question: str,
        k: int = 5
    ) -> dict:
        """
        Handle a legal question — routes to Retrieval Agent.
        
        Args:
            question: Legal question
            k: Number of sections to retrieve
        
        Returns:
            dict: answer, sources, status
        """
        print(f"\n🤖 Orchestrator received: '{question[:50]}...'")
        
        agent_type = self.route(question)
        print(f"   → Routing to: {agent_type} agent")
        
        if agent_type == 'document':
            # Cannot handle document from just a question
            # Return helpful message
            return {
                'agent'   : self.name,
                'question': question,
                'answer'  : "It seems you want to generate a document. "
                            "Please use the /generate-doc endpoint with "
                            "doc_type, party1, party2 and terms.",
                'sources' : [],
                'status'  : 'redirect'
            }
        
        elif agent_type == 'research':
            result = self.research_agent.run(question)
            return {
                'agent'   : result['agent'],
                'question': question,
                'answer'  : result['research'],
                'sources' : [],
                'status'  : result['status']
            }
        
        else:
            return self.retrieval_agent.run(question, k=k)
    
    def handle_document(
        self,
        doc_type: str,
        party1: str,
        party2: str,
        terms: str,
        extra_details: str = ""
    ) -> dict:
        """
        Handle document generation request.
        Always routes to Document Agent.
        
        Returns:
            dict: document, filename, status
        """
        print(f"\n🤖 Orchestrator: Document request")
        print(f"   → Routing to: Document Agent")
        
        return self.document_agent.run(
            doc_type=doc_type,
            party1=party1,
            party2=party2,
            terms=terms,
            extra_details=extra_details
        )
    
    def handle_research(self, topic: str) -> dict:
        """
        Handle research request.
        Always routes to Research Agent.
        
        Returns:
            dict: research, status
        """
        print(f"\n🤖 Orchestrator: Research request")
        print(f"   → Routing to: Research Agent")
        
        return self.research_agent.run(topic)
    
    def get_system_info(self) -> dict:
        """Return information about all agents"""
        return {
            'orchestrator': self.name,
            'agents': [
                {
                    'name'       : self.retrieval_agent.name,
                    'description': self.retrieval_agent.description
                },
                {
                    'name'       : self.document_agent.name,
                    'description': self.document_agent.description,
                    'documents'  : self.document_agent.get_supported_documents()
                },
                {
                    'name'         : self.research_agent.name,
                    'description'  : self.research_agent.description,
                    'research_areas': self.research_agent.get_research_areas()
                }
            ]
        }