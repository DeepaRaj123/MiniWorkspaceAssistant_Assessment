from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from groq import Groq
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

print("✅ Groq client initialized")

# -----------------------------
# Flask App Setup
# -----------------------------
app = Flask(__name__)

DOCUMENT_STORE = []
document_chunks = []

# -----------------------------
# Embeddings + FAISS Setup
# -----------------------------
print("🔄 Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

embedding_dim = 384
faiss_index = faiss.IndexFlatL2(embedding_dim)

print("✅ FAISS index ready")

# -----------------------------
# Groq LLM Function
# -----------------------------
def ask_llm(question, context_chunks):
    context = "\n\n".join(context_chunks)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful workspace assistant. Answer clearly and concisely using the provided context."
        },
        {
            "role": "user",
            "content": f"""
Context:
{context}

Question:
{question}
"""
        }
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.2,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        app.logger.error(str(e))
        raise RuntimeError("LLM request failed")


# -----------------------------
# Routes
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        text = file.read().decode("utf-8")
    except Exception:
        return jsonify({"error": "Only UTF-8 text files supported"}), 400

    # Chunk text
    chunks = [text[i:i + 300] for i in range(0, len(text), 300)]

    # Generate embeddings
    embeddings = embedding_model.encode(chunks)
    faiss_index.add(np.array(embeddings).astype("float32"))

    document_chunks.extend(chunks)

    for chunk in chunks:
        DOCUMENT_STORE.append({
            "text": chunk,
            "source": file.filename
        })

    return jsonify({
        "message": "File uploaded successfully",
        "chunks_added": len(chunks)
    })

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    question = data.get("question") if data else None

    if not question:
        return jsonify({"error": "Question required"}), 400

    if not document_chunks:
        return jsonify({"error": "Upload documents first"}), 400

    # Embed question
    q_embedding = embedding_model.encode([question])

    # Search FAISS
    k = min(3, len(document_chunks))
    _, indices = faiss_index.search(
        np.array(q_embedding).astype("float32"), k
    )

    context = [document_chunks[i] for i in indices[0]]

    # Ask LLM
    answer = ask_llm(question, context)

    return jsonify({
        "question": question,
        "answer": answer,
        "sources": context
    })

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting Flask app with Groq LLM...")
    app.run(debug=True)
