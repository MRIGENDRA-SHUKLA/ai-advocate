# AI Advocate — Multi-Agent RAG Legal Assistant

> A production-ready AI system that answers Indian legal questions,
> drafts legal documents, and performs legal research using
> 56,617 chunks from 855 unique Indian Acts.

---

## What it does

- **Ask legal questions** → Get answers with exact Act and Section citations
- **Draft legal documents** → Rental agreements, NDAs, employment contracts
- **Legal research** → Comprehensive research on any Indian legal topic
- **REST API** → 5 endpoints with auto-generated Swagger documentation

---

## Tech Stack

```
Data          → pandas, openpyxl
Vector DB     → FAISS (56,617 vectors, 384 dimensions)
Embeddings    → sentence-transformers (all-MiniLM-L6-v2)
LLM           → Groq (llama-3.3-70b-versatile)
RAG           → HyDE + semantic search + retry logic
Agents        → Custom orchestrator with 3 specialist agents
API           → FastAPI + uvicorn
Evaluation    → Custom Ragas-style metrics + LLM-as-Judge
```

---

## Project Structure

```
11_AI_ADVOCATE/
├── notebooks/
│   ├── 00_setup.ipynb                  ← Install libraries
│   ├── 01_data_exploration.ipynb       ← Explore 30,444 sections
│   ├── 02_data_cleaning.ipynb          ← Clean + chunk data
│   ├── 03_embeddings_faiss.ipynb       ← Build vector database
│   ├── 04_rag_pipeline.ipynb           ← RAG + HyDE pipeline
│   ├── 05_multi_agent.ipynb            ← Multi-agent system
│   ├── 06_document_generation.ipynb    ← Legal document drafting
│   ├── 07_fastapi_prototype.ipynb      ← REST API
│   └── 08_evaluation.ipynb             ← Ragas + LLM-as-Judge
├── data/
│   ├── Scrapmetadata_forvectordatabase.xlsx
│   └── processed_chunks.json
├── vector_store/
│   ├── legal_index.faiss (82.94 MB)
│   └── metadata.json (38.04 MB)
├── outputs/                            ← Generated documents
├── evaluation/                         ← Evaluation reports
├── .env                                ← API keys (never commit!)
├── .gitignore
├── requirements.txt
└── claude.md
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-advocate.git
git clone   https://github.com/MRIGENDRA-SHUKLA/ai-advocate
cd ai-advocate
```

### 2. Install libraries
```bash
pip install pandas faiss-cpu sentence-transformers
pip install google-genai groq ragas fastapi uvicorn
pip install python-dotenv datasets numpy openpyxl
pip install nest-asyncio pydantic ipykernel
```

### 3. Set up API keys
Create a `.env` file in root folder:
```
GOOGLE_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
```

Get free API keys from:
- Gemini → https://aistudio.google.com/api-keys
- Groq → https://console.groq.com

### 4. Add your data
Place `Scrapmetadata_forvectordatabase.xlsx` in `data/` folder

---

## How to Run

Run notebooks **in order** — each depends on previous:

```
Step 1 → 00_setup.ipynb               (run once)
Step 2 → 01_data_exploration.ipynb    (understand data)
Step 3 → 02_data_cleaning.ipynb       (creates processed_chunks.json)
Step 4 → 03_embeddings_faiss.ipynb    (creates legal_index.faiss) ⚠️ 15-20 min
Step 5 → 04_rag_pipeline.ipynb        (RAG pipeline)
Step 6 → 05_multi_agent.ipynb         (multi-agent system)
Step 7 → 06_document_generation.ipynb (document drafting)
Step 8 → 07_fastapi_prototype.ipynb   (REST API)
Step 9 → 08_evaluation.ipynb          (evaluation)
```

⚠️ Notebook 03 takes 15-20 minutes — it embeds 56,617 chunks!

---

## API Endpoints

Start the server by running `07_fastapi_prototype.ipynb`
then visit: **http://127.0.0.1:8000/docs**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | System status |
| POST | /ask | Ask legal question |
| POST | /generate-doc | Generate legal document |
| POST | /research | Research legal topic |
| GET | /stats | System statistics |

### Example Request
```json
POST /ask
{
  "question": "What is the punishment for murder in India?",
  "k": 5
}
```

### Example Response
```json
{
  "question": "What is the punishment for murder in India?",
  "answer": "Under Section 302 of the Indian Penal Code,
             murder is punishable with death or imprisonment
             for life, and also liable to fine.",
  "sources": ["THE INDIAN PENAL CODE — Section 302"],
  "status": "success"
}
```

---

## Dataset

| Property | Value |
|----------|-------|
| Source | 855 unique Indian Acts |
| Original rows | 30,444 sections |
| After cleaning | 29,992 sections |
| After chunking | 56,617 chunks |
| Top Act | Income Tax Act 1961 (416 sections) |
| Chunk size | 500 chars with 50 char overlap |

---

## Multi-Agent System

```
User Query
    ↓
Orchestrator (Boss Agent)
    ↓
┌─────────────────────────────────────────┐
│  "draft/contract" → Document Agent      │
│  "research/explain" → Research Agent    │
│  everything else → Retrieval Agent      │
└─────────────────────────────────────────┘
    ↓
Answer with sources
```

---

## Evaluation Results

| Metric | Score | Grade |
|--------|-------|-------|
| Faithfulness | 0.440 | ACCEPTABLE ⚠️ |
| Answer Relevancy | 0.720 | GOOD ✅ |
| Context Recall | 0.130 | NEEDS IMPROVEMENT ❌ |
| LLM Judge Score | 6.7/10 | GOOD ✅ |

**Key Finding:** Low Context Recall proves HyDE implementation
is critical — basic retrieval finds superficially similar but
legally irrelevant sections.

---

## Documents Generated

| Document | Indian Law Referenced |
|----------|----------------------|
| Rental Agreement | Transfer of Property Act 1882 |
| Non Disclosure Agreement | Indian Contract Act 1872 |
| Employment Contract | Industrial Employment Act 1946 |
| Partnership Deed | Indian Partnership Act 1932 |
| Service Agreement | Indian Contract Act 1872 |

---

## Future Improvements

- [ ] HyDE with real Gemini → improve Context Recall from 0.13 to 0.6+
- [ ] Re-ranking with cross-encoder
- [ ] Web search with Tavily API for real-time legal news
- [ ] Docker containerization for Cloud Run deployment
- [ ] Streamlit/Gradio frontend UI
- [ ] Official Ragas evaluation with OpenAI key
- [ ] More document types (Will, Affidavit, Power of Attorney)

---

## Environment

```
OS      : Windows 11
Python  : 3.12.10
Editor  : VS Code with Jupyter extension
LLM     : Groq llama-3.3-70b-versatile
Embeddings: all-MiniLM-L6-v2 (384 dims)
FAISS   : IndexFlatL2
```

---

## Security

- API keys stored in `.env` file only
- `.env` added to `.gitignore`
- Keys never hardcoded in notebooks
- Rotate keys immediately if exposed

---

## Author

**Maggi**
AI/ML Engineer | GenAI Enthusiast
Target: AI-focused companies in India

---

*Built with ❤️ using Python, FAISS, Groq, and FastAPI*
