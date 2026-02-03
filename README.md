🧠 Mini Workspace Assistant
AI Agent with RAG (Retrieval-Augmented Generation)
Engineering Assignment – Senior Software Engineer

📌 Overview
The Mini Workspace Assistant is a lightweight AI agent that allows users to upload documents and ask questions about their content using semantic search and an LLM.

This project demonstrates:
    - Retrieval-Augmented Generation (RAG)
    - Vector embeddings and similarity search
    - LLM API integration
    - Clean, pragmatic backend design with Flask

🏗️ Architecture Overview
    Document Upload
    ↓
    Text Extraction & Chunking
    ↓
    Embeddings (Sentence Transformers)
    ↓
    Vector Database (FAISS)
    ↓
    User Question
    ↓
    Semantic Search (FAISS)
    ↓
    Relevant Chunks
    ↓
    LLM (Groq)
    ↓
    Final Answer

🚀 Features Implemented
    1. Document Upload & Processing

        - Upload .txt files via API
        - Extracts text content
        - Splits documents into fixed-size chunks
        - Stores chunks in memory

    2. Vector Search (Semantic Retrieval)

        - Uses SentenceTransformers (all-MiniLM-L6-v2) for embeddings
        - Stores embeddings in FAISS (in-memory vector database)
        - Performs similarity search to retrieve relevant chunks

    3. LLM Integration

        - Uses Groq API (OpenAI-compatible, fast, free tier)
        - Sends retrieved chunks + user question to the LLM
        - Returns concise, context-aware answers

    4. Clean API Design

        - /upload – upload documents
        - /query – ask questions
        - /health – health check

🛠️ Tech Stack & Decisions
    Component	        Choice	                 Reason
    Backend	            Flask	                 Lightweight, simple, production-friendly
    Embeddings	        SentenceTransformers	 Free, fast, no external dependency
    Vector DB	        FAISS	                 Lightweight, ideal for local semantic search
    LLM	                Groq (Llama 3.1)	     OpenAI-style API, fast, stable, free tier
    Language	        Python 3.10+	         Ecosystem maturity
   
📂 Project Structure
    mini-workspace-assistant/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── .env.example
    └── test.txt

⚙️ Setup Instructions
    1️⃣ Clone Repository
        git clone <your-repo-url>
        cd mini-workspace-assistant

    2️⃣ Create Virtual Environment
        python3 -m venv venv
        source venv/bin/activate

    3️⃣ Install Dependencies
        pip install -r requirements.txt

    🔑 Environment Variables

        Create a .env file:
        GROQ_API_KEY=your_groq_api_key_here
        You can get a free API key from https://console.groq.com

    ▶️ Run the Application
        python3 app.py


App runs on:

http://127.0.0.1:5000

    📡 API Endpoints

    ✅ Health Check
    GET /health

        Response:
        { "status": "ok" }

    📤 Upload Document
    POST /upload

        Form-Data
        file: .txt file

        Response:
        {
        "message": "File uploaded successfully",
        "chunks_added": 3
        }

    ❓ Ask a Question
    POST /query

        Body
        {
        "question": "Summarize this document"
        }

        Response:
        {
        "question": "Summarize this document",
        "answer": "This document explains...",
        "sources": ["Relevant document chunks..."]
        }

🧠 RAG Implementation Details

    - Documents are chunked and embedded using SentenceTransformers
    - Embeddings are stored in FAISS (vector database)
    - User queries are embedded and semantically matched
    - Top-K relevant chunks are sent to the LLM
    - LLM generates a context-aware response
    - This ensures answers are grounded in uploaded documents, not hallucinated.

⚠️ Assumptions & Limitations

    - Only .txt files supported (PDF can be added easily)
    - In-memory storage (not persistent)
    - Not optimized for very large datasets
    - Single-user / single-session design

🧪 Sample Test
curl -X POST http://127.0.0.1:5000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Summarize this document"}'

⏱️ Estimated Time Spent
~ 6–7 hours

📝 Notes

    - Focused on correctness and clarity over over-engineering
    - Chose lightweight tools to move fast
    - Architecture can easily be extended with:
    - Persistent DB
    - PDF support
    - Auth
    - Streaming responses

✅ Assignment Status
Requirement	     Status
Document Upload	 ✅
Chunking	     ✅
Vector Search	 ✅
LLM Integration	 ✅
RAG Flow	     ✅
Clean Code	     ✅
README	         ✅

🏁 Final Thoughts
This project demonstrates a production-ready, minimal RAG system built with pragmatic technical choices and clean design.