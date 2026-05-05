# api/agents/research_agent.py
import os
from services.generator import generate_legal_research

class ResearchAgent:
    """
    Specialist agent for legal research.
    Provides comprehensive research on any Indian legal topic.
    
    Called when user wants to RESEARCH a legal topic.
    Example: "What is FIR in Indian law?"
    Example: "Explain Section 498A IPC"
    """
    
    def __init__(self):
        self.name = "Research Agent"
        self.description = "Provides comprehensive Indian legal research"
        self.research_areas = [
            "Criminal Law (IPC, CrPC)",
            "Civil Law (CPC)",
            "Corporate Law (Companies Act)",
            "Tax Law (Income Tax, GST)",
            "Labour Law",
            "Constitutional Law",
            "Property Law",
            "Family Law",
            "Consumer Protection Law",
            "Cyber Law (IT Act)"
        ]
    
    def run(self, topic: str) -> dict:
        """
        Research a legal topic comprehensively.
        
        Args:
            topic: Legal topic to research
        
        Returns:
            dict: research, agent name, status
        """
        print(f"🌐 Research Agent activated!")
        print(f"   Topic: {topic[:60]}...")
        
        try:
            # Generate research
            research = generate_legal_research(topic)
            
            # Save research to outputs
            filename = self._save_research(topic, research)
            
            print(f"✅ Research generated!")
            print(f"   Length  : {len(research)} characters")
            print(f"   Saved to: {filename}")
            
            return {
                'agent'   : self.name,
                'topic'   : topic,
                'research': research,
                'saved_to': filename,
                'length'  : len(research),
                'status'  : 'success'
            }
        
        except Exception as e:
            print(f"❌ Research Agent error: {str(e)}")
            return {
                'agent'   : self.name,
                'topic'   : topic,
                'research': f"Error: {str(e)}",
                'saved_to': '',
                'length'  : 0,
                'status'  : 'error'
            }
    
    def _save_research(self, topic: str, research: str) -> str:
        """
        Save research to outputs folder.
        
        Args:
            topic: Research topic
            research: Research content
        
        Returns:
            str: filename where saved
        """
        try:
            os.makedirs('outputs', exist_ok=True)
            
            # Clean topic for filename
            clean_topic = topic[:30].replace(
                ' ', '_').replace('/', '_')
            filename = f"outputs/research_{clean_topic}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Research Topic: {topic}\n")
                f.write("=" * 60 + "\n\n")
                f.write(research)
            
            return filename
        
        except Exception as e:
            print(f"⚠️ Could not save research: {e}")
            return ""
    
    def get_research_areas(self) -> list:
        """Return list of research areas covered"""
        return self.research_areas