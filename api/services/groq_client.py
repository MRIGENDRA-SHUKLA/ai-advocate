# api/services/groq_client.py
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Initialize Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)

# Model to use
GROQ_MODEL = "llama-3.3-70b-versatile"

def call_groq(prompt: str, system_prompt: str = None) -> str:
    """
    Send a prompt to Groq and get a response.
    Has retry logic for reliability.
    
    Args:
        prompt: The user prompt
        system_prompt: Optional system instructions
    
    Returns:
        str: Groq response text
    """
    # Default system prompt
    if not system_prompt:
        system_prompt = "You are an expert Indian legal assistant."
    
    # Try up to 3 times
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # low = more consistent answers
                max_tokens=2048
            )
            return response.choices[0].message.content

        except Exception as e:
            wait_time = (attempt + 1) * 10
            print(f"⚠️ Groq attempt {attempt+1} failed: {str(e)[:50]}")
            
            if attempt < 2:
                import time
                print(f"⏳ Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return "Service temporarily unavailable. Please try again."

def test_connection() -> bool:
    """Test if Groq connection is working"""
    try:
        response = call_groq("Say: Groq connected!")
        return "connected" in response.lower()
    except:
        return False