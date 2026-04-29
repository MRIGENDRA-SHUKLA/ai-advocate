# Claude.md — AI Advocate Multi-Agent System

## Project Overview
AI Advocate is a RAG-based Multi-Agent Legal Assistant that answers legal questions
using 56,617 chunks from 855 unique Indian Acts (30,444 original sections).
The system uses FAISS for semantic search, Gemini for answer generation,
and a multi-agent orchestrator to handle different types of legal tasks.

---

## Project Structure
```
11_AI_ADVOCATE/
├── notebooks/
│   ├── 00_setup.ipynb                  ← Install libraries, create folders
│   ├── 01_data_exploration.ipynb       ← Explore 30,444 legal sections
│   ├── 02_data_cleaning.ipynb          ← Clean, chunk, save JSON
│   ├── 03_embeddings_faiss.ipynb       ← Build FAISS vector database
│   ├── 04_rag_pipeline.ipynb           ← HyDE + Reranking + Gemini RAG
│   ├── 05_multi_agent.ipynb            ← Orchestrator + 3 agents
│   ├── 06_document_generation.ipynb    ← Draft legal contracts
│   ├── 07_fastapi_prototype.ipynb      ← API endpoints prototype
│   └── 08_evaluation.ipynb             ← Ragas + LLM-as-Judge
├── data/
│   ├── Scrapmetadata_forvectordatabase.xlsx  ← Raw source data
│   └── processed_chunks.json                 ← 56,617 cleaned chunks
├── vector_store/
│   ├── legal_index.faiss               ← FAISS vector database
│   └── metadata.json                   ← Chunk ID to metadata mapping
├── outputs/
│   └── sample_rental_agreement.txt     ← Generated legal documents
├── evaluation/
│   ├── eval_questions.json             ← 20 test questions
│   └── ragas_report.json               ← Evaluation scores
├── requirements.txt                    ← All Python libraries
└── README.md                           ← Project documentation
```

---

## Dataset Details
- **Source file**: Scrapmetadata_forvectordatabase.xlsx
- **Original rows**: 30,444 legal sections
- **After cleaning**: 29,992 sections (452 empty/short rows removed)
- **After chunking**: 56,617 chunks (chunk size=500, overlap=50)
- **Unique Acts**: 855 Indian Acts
- **Top Act**: Income Tax Act 1961 (416 sections)
- **Content length**: 3 to 12,436 characters, average 614

### Columns in Dataset
| Column | Description | Missing Values |
|--------|-------------|----------------|
| Act Title | Name of the Indian Act | 0 |
| Act ID | Act number and year | 0 |
| Act Definition | Brief definition of Act | 209 |
| Enactment Date | Date Act was passed | 0 |
| Chapter ID | Chapter number | 7,569 |
| Chapter Name | Chapter name | 6,542 |
| Section ID | Section number | 0 |
| Section Heading | Section title | 0 |
| Content | Full legal text | 450 |

---

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.12.10 | Core programming language |
| pandas 3.0.2 | Data loading and cleaning |
| faiss-cpu 1.13.2 | Vector database for semantic search |
| sentence-transformers 5.4.1 | Convert text to embeddings |
| google.genai | Gemini LLM for answer generation |
| google-cloud-aiplatform | Vertex AI integration |
| ragas | RAG evaluation metrics |
| nest-asyncio | Run async code in notebooks |
| python-dotenv | Load API keys from .env |
| numpy 2.4.4 | Array operations |
| openpyxl | Read Excel files |

---

## Notebooks — What Each Does

### 00_setup.ipynb
- Install all libraries with pip
- Verify all imports work
- Create project folder structure
- Install correct google.genai package

### 01_data_exploration.ipynb ✅ COMPLETE
- Load Excel file with pandas
- Check all 9 column names
- Preview first 5 rows
- Count 855 unique Acts
- Find missing values (450 Content missing)
- Analyze content length distribution
- Read one full legal section
- Summary of findings

### 02_data_cleaning.ipynb ✅ COMPLETE
- Remove 450 rows with empty Content
- Remove rows with less than 10 characters
- Clean text (extra spaces, newlines, tabs)
- Chunk all sections (size=500, overlap=50)
- Save 56,617 chunks to processed_chunks.json
- Verify JSON saved correctly

### 03_embeddings_faiss.ipynb ✅ COMPLETE
- Loaded 56,617 chunks
- Embedded with all-MiniLM-L6-v2 (384 dimensions)
- Built FAISS IndexFlatL2
- Saved legal_index.faiss (82.94 MB)
- Saved metadata.json (38.04 MB)
- Tested search — working perfectly!

### 04_rag_pipeline.ipynb ⏳ PENDING
- Load FAISS index
- Basic retrieval function
- HyDE (Hypothetical Document Embeddings)
- Re-ranking with cross-encoder
- Connect to Gemini via google.genai
- Full RAG pipeline: question → retrieve → generate
- Test with sample legal questions

### 05_multi_agent.ipynb ⏳ PENDING
- RetrievalAgent (searches FAISS)
- DocumentAgent (drafts contracts)
- ResearchAgent (web search)
- Orchestrator (routes to correct agent)
- Full system test

### 06_document_generation.ipynb ⏳ PENDING
- Draft rental agreements
- Draft NDAs
- Draft employment contracts
- Save outputs to outputs/ folder

### 07_fastapi_prototype.ipynb ⏳ PENDING
- Define /ask endpoint
- Define /generate-doc endpoint
- Define /health endpoint
- Test with requests library

### 08_evaluation.ipynb ⏳ PENDING
- Create 20 test questions
- Run Ragas metrics (Faithfulness, Relevancy, Context Recall)
- Run LLM-as-Judge scoring
- Save ragas_report.json

---

## Key Concepts for Interview

### What is RAG?
Retrieval Augmented Generation. Instead of asking Gemini a question directly,
we first RETRIEVE relevant law sections from FAISS, then pass them to Gemini
as context. This grounds the answer in real law — no hallucination.

### What is FAISS?
Facebook AI Similarity Search. A vector database that stores 56,617 chunk
embeddings and finds the most similar chunks to any query in milliseconds.

### What is HyDE?
Hypothetical Document Embeddings. Instead of searching with the user question,
we ask Gemini to generate a fake answer first, then search FAISS with that
fake answer. This improves retrieval accuracy significantly.

### What is Chunking?
Splitting long legal sections into 500 character pieces with 50 character
overlap. Needed because FAISS works best with uniform sized chunks and
LLMs have context window limits.

### What is Re-ranking?
After FAISS returns top 20 results, a cross-encoder model re-scores them
to pick the best 5. More accurate than FAISS alone.

### What is Ragas?
A framework to evaluate RAG systems. Key metrics:
- Faithfulness: Is the answer grounded in retrieved context?
- Answer Relevancy: Does the answer address the question?
- Context Recall: Did we retrieve the right chunks?

### What is Multi-Agent?
Instead of one big function, we have specialist agents:
- Orchestrator: Boss — decides which agent to call
- RetrievalAgent: Searches FAISS for relevant law
- DocumentAgent: Drafts legal contracts using Gemini
- ResearchAgent: Real-time web search for current legal news

---

## Environment Setup
```bash
# Python version
Python 3.12.10

# Install all libraries
pip install pandas faiss-cpu sentence-transformers google-genai
pip install google-cloud-aiplatform ragas nest-asyncio requests
pip install python-dotenv datasets numpy openpyxl ipykernel

# Environment variables needed in .env file
GOOGLE_API_KEY=your_key_here
VERTEX_PROJECT_ID=your_project_id
```

---

## Data Flow
```
Excel File (30,444 rows)
        ↓
  [02_data_cleaning.ipynb]
        ↓
processed_chunks.json (56,617 chunks)
        ↓
  [03_embeddings_faiss.ipynb]
        ↓
legal_index.faiss + metadata.json
        ↓
  [04_rag_pipeline.ipynb]
        ↓
User Question → FAISS Search → HyDE → Rerank → Gemini → Answer
        ↓
  [05_multi_agent.ipynb]
        ↓
Orchestrator → Routes to correct Agent → Returns Result
        ↓
  [08_evaluation.ipynb]
        ↓
Ragas Scores + LLM Judge Report
```

---

## Important Notes for Claude
- Editor: VS Code with Jupyter extension
- Python: 3.12.10
- OS: Windows
- Use `google.genai` NOT `google.generativeai` (deprecated)
- All notebooks are in `notebooks/` subfolder
- Data files are in `data/` subfolder
- Vector store files are in `vector_store/` subfolder
- Each notebook loads data fresh — no shared state between notebooks
- Chunk size is 500 characters with 50 character overlap
- Embedding model: all-MiniLM-L6-v2 from sentence-transformers
- FAISS index type: IndexFlatL2
- Teaching style: Step by step, one cell at a time, simple language

use model="gemini-2.5-flash" -- in 04_rag_pipeline.ipynb filr for API 