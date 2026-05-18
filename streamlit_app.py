import os
import json
import time
import streamlit as st
import faiss
import numpy as np
from groq import Groq
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv('.env', override=True)

st.set_page_config(
    page_title="AI Advocate — Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# ── Cached loaders ────────────────────────────────────────────────

@st.cache_resource
def load_faiss():
    index = faiss.read_index('vector_store/legal_index.faiss')
    with open('vector_store/metadata.json', 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    return index, chunks

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def load_groq_client():
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return None
    return Groq(api_key=api_key)

# ── Core pipeline ─────────────────────────────────────────────────

def call_groq(client, prompt, system="You are an expert Indian legal assistant."):
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception:
            if attempt < 2:
                time.sleep((attempt + 1) * 10)
    return "Service temporarily unavailable. Please try again."

def retrieve(query, index, chunks, embedding_model, k=5):
    query_vector = embedding_model.encode([query]).astype('float32')
    distances, indices = index.search(query_vector, k=k)
    results = []
    for i, idx in enumerate(indices[0]):
        chunk = chunks[idx]
        results.append({
            'rank'    : i + 1,
            'distance': round(float(distances[0][i]), 4),
            'act'     : chunk['act_title'],
            'section' : chunk['section_id'],
            'heading' : chunk['section_heading'],
            'text'    : chunk['text']
        })
    return results

def retrieval_agent(question, index, chunks, embedding_model, groq_client):
    results = retrieve(question, index, chunks, embedding_model, k=5)
    context = ""
    sources = []
    for r in results:
        context += (
            f"\nAct: {r['act']}\n"
            f"Section: {r['section']} - {r['heading']}\n"
            f"Text: {r['text']}\n"
        )
        sources.append(f"{r['act']} — {r['section']} {r['heading']}")

    prompt = f"""Answer this Indian legal question based on these law sections.
Cite exact Act and Section numbers. Use simple clear language.

LAW SECTIONS:
{context}

QUESTION: {question}"""

    answer = call_groq(groq_client, prompt)
    return answer, sources, "Retrieval Agent"

def document_agent(request, groq_client):
    prompt = f"""You are an expert Indian legal document drafter.
Draft a professional legal document based on this request.

Request: {request}

Include all of: Title and Date, Parties Involved, Terms and Conditions,
Payment Details (if applicable), Duration, Termination Clause,
Governing Law (Indian law), Signatures Section.

Make it professional and legally sound under Indian law."""

    document = call_groq(groq_client, prompt)

    os.makedirs('outputs', exist_ok=True)
    with open('outputs/generated_document.txt', 'w', encoding='utf-8') as f:
        f.write(document)

    return document, [], "Document Agent"

def research_agent(topic, groq_client):
    prompt = f"""You are an expert Indian legal researcher.
Provide a comprehensive summary on this topic under Indian law.

Topic: {topic}

Include:
1. Overview under Indian law
2. Relevant Acts and Sections
3. Key legal provisions
4. Practical implications
5. Important case references if known

Be specific and cite Indian laws."""

    research = call_groq(groq_client, prompt)
    return research, [], "Research Agent"

def orchestrate(user_input, index, chunks, embedding_model, groq_client):
    text = user_input.lower()

    doc_keywords      = ['draft', 'create', 'write', 'agreement', 'contract',
                         'nda', 'document', 'deed', 'lease', 'rental', 'employment', 'format']
    research_keywords = ['research', 'explain', 'what is', 'tell me', 'describe',
                         'overview', 'summary', 'about', 'how does', 'define', 'meaning']

    if any(kw in text for kw in doc_keywords):
        return document_agent(user_input, groq_client)
    elif any(kw in text for kw in research_keywords):
        return research_agent(user_input, groq_client)
    else:
        return retrieval_agent(user_input, index, chunks, embedding_model, groq_client)

# ── Sidebar ───────────────────────────────────────────────────────

with st.sidebar:
    st.header("System Status")

    index, chunks = None, None
    embedding_model = None
    groq_client = None

    try:
        index, chunks = load_faiss()
        st.success(f"FAISS: {index.ntotal:,} vectors")
    except Exception as e:
        st.error(f"FAISS: {str(e)[:50]}")

    try:
        embedding_model = load_embedding_model()
        st.success("Embedding: all-MiniLM-L6-v2")
    except Exception as e:
        st.error(f"Embedding: {str(e)[:50]}")

    groq_client = load_groq_client()
    if groq_client:
        st.success("Groq: LLaMA 3.3 70B ready")
    else:
        st.error("Groq: GROQ_API_KEY missing in .env")

    st.divider()
    st.markdown("**Dataset**")
    st.markdown("- 56,617 law chunks")
    st.markdown("- 855 Indian Acts")
    st.markdown("- 30,444 legal sections")

    st.divider()
    st.markdown("**Agents**")
    st.markdown("🔍 **Retrieval** — finds relevant law sections")
    st.markdown("📝 **Document** — drafts contracts & agreements")
    st.markdown("🌐 **Research** — explains legal topics")

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# ── Main UI ───────────────────────────────────────────────────────

st.title("⚖️ AI Advocate")
st.caption("Indian Legal Assistant — RAG + Multi-Agent | 855 Acts | Groq LLaMA 3.3 70B")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Example prompts shown only on empty chat
if not st.session_state.messages:
    st.markdown("### Try an example:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚖️ Punishment for murder?"):
            st.session_state.pending = "What is the punishment for murder in India?"
            st.rerun()
    with col2:
        if st.button("📄 Draft a rental agreement"):
            st.session_state.pending = (
                "Draft a rental agreement between Rahul Sharma (Landlord) "
                "and Priya Singh (Tenant) for a flat in Mumbai, "
                "rent 15000 per month, 11 month agreement, 2 month deposit"
            )
            st.rerun()
    with col3:
        if st.button("🔍 What is FIR?"):
            st.session_state.pending = "What is the meaning of FIR in Indian law?"
            st.rerun()

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- {s}")
        if msg.get("agent"):
            st.caption(f"Handled by: {msg['agent']}")

# Consume pending prompt from example buttons
pending = st.session_state.pop("pending", None)
user_input = (
    st.chat_input("Ask a legal question, request a document draft, or research a topic...")
    or pending
)

if user_input:
    if not all([index, chunks, embedding_model, groq_client]):
        st.error("System not fully loaded — check the sidebar for errors.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                answer, sources, agent_name = orchestrate(
                    user_input, index, chunks, embedding_model, groq_client
                )
            st.markdown(answer)
            if sources:
                with st.expander("📚 Sources"):
                    for s in sources:
                        st.markdown(f"- {s}")
            st.caption(f"Handled by: {agent_name}")

        st.session_state.messages.append({
            "role"   : "assistant",
            "content": answer,
            "sources": sources,
            "agent"  : agent_name
        })
