## Challenges & Solutions faced in 04_rag_pipeline.ipynb

---

### Challenge 1 — API Key Exposed Publicly
**Problem:**
- Accidentally shared real Gemini API key in public chat
- Someone used the key and exhausted entire free quota
- Got 429 RESOURCE_EXHAUSTED error immediately

**Solution:**
- Deleted compromised key immediately from Google AI Studio
- Created fresh API key
- Stored key ONLY in .env file
- Added .env to .gitignore so it never goes to GitHub

**Lesson Learned:**
- Never share API keys anywhere except .env file
- If key is exposed even for 1 second → delete and rotate immediately
- This is standard security practice in all real companies

---

### Challenge 2 — Wrong Google Package
**Problem:**
- Used old `google.generativeai` package
- Got FutureWarning: "All support has ended"
- Package was deprecated by Google

**Solution:**
- Uninstalled old package: pip uninstall google-generativeai
- Installed new package: pip install google-genai
- Updated all imports to: from google import genai

**Lesson Learned:**
- Always check for deprecated packages
- Google renamed their SDK from google.generativeai → google.genai

---

### Challenge 3 — Quota Exhausted (429 Error)
**Problem:**
- Free tier allows only 15 requests per minute
- Kept retrying quickly after errors
- Got: ClientError 429 RESOURCE_EXHAUSTED
- limit: 0 for all models

**Solution:**
- Added time.sleep(5) before every Gemini call
- Added time.sleep(30) between multiple questions
- Built retry logic with exponential backoff
- Waited 1-2 minutes before retrying after 429 error

**Lesson Learned:**
- Free tier has strict rate limits
- Always add sleep() between API calls
- Exponential backoff is standard production pattern

---

### Challenge 4 — Wrong Gemini Model (404 Error)
**Problem:**
- Used model="gemini-1.5-flash-8b"
- Got: ClientError 404 NOT_FOUND
- "models/gemini-1.5-flash-8b is not found"
- Model not available in India region

**Solution:**
- Listed all available models using client.models.list()
- Found gemini-2.5-flash works for our account
- Updated all model references to gemini-2.5-flash

**Lesson Learned:**
- Not all Gemini models are available in all regions
- Always verify model availability for your region
- gemini-2.5-flash is best available model for India free tier

---

### Challenge 5 — Server Unavailable (503 Error)
**Problem:**
- Got: ServerError 503 UNAVAILABLE
- "This model is currently experiencing high demand"
- System crashed on first failure

**Solution:**
- Built retry logic with 3 attempts
- Added increasing wait times between retries:
  Attempt 1 fails → wait 30 seconds
  Attempt 2 fails → wait 60 seconds
  Attempt 3 fails → wait 90 seconds

**Lesson Learned:**
- Production AI systems always need retry logic
- 503 means server busy, not your fault
- Exponential backoff prevents overwhelming the server

---

### Challenge 6 — Variable Name Clash
**Problem:**
- SentenceTransformer model and Gemini both named "model"
- Got: AttributeError: Model object has no attribute encode
- Python was calling Gemini model instead of embedding model

**Solution:**
- Renamed SentenceTransformer variable to "embedding_model"
- Clear separation between embedding_model and Gemini client
- No more variable name conflicts

**Lesson Learned:**
- Always use descriptive variable names
- embedding_model for SentenceTransformer
- client for Gemini connection

---

### Challenge 7 — Poor Retrieval Quality
**Problem:**
- FAISS returning military/security act sections
- For "punishment for theft" → got Border Security Force Act
- Gemini answered "no specific information found"

**Solution:**
- Enhanced query with legal terminology before FAISS search
- Added "Indian law legal section" prefix to all queries
- Real fix → HyDE with Gemini generates proper legal terms
  before searching FAISS → much better retrieval

**Lesson Learned:**
- Plain natural language queries dont match legal terminology
- Query enrichment significantly improves retrieval accuracy
- HyDE is critical for domain-specific RAG systems like legal AI

---

### Overall Interview Answer:
> "During development we faced 7 major challenges including
> API security breach, deprecated packages, rate limiting,
> regional model availability, server failures, variable conflicts
> and poor retrieval quality. Each challenge taught us something
> important — from API key rotation practices to implementing
> exponential backoff retry logic and query enrichment techniques.
> These real-world problems made the system more robust and
> production-ready."