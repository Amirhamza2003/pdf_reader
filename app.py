import streamlit as st
import fitz  # PyMuPDF
import os
import requests
from PIL import Image
import re

# Streamlit page config

st.set_page_config(page_title="PDF Q&A Chatbot", page_icon="📄", layout="centered")

st.title("📄 PDF Q&A Chatbot")
st.markdown(
"""
Upload a large PDF (500+ pages), extract its content, and ask questions about it using Groq's Llama 3 model.
"""
)

# --- API KEY ---

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or st.text_input(
    "Enter your Groq API Key", type="password"
)

def ask_groq(question, context):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant answering questions based only on the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ Error: {e}"

def chunk_text(text, chunk_size=1000, overlap=200):
    """Split text into overlapping chunks for large PDF handling"""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def extract_pdf(pdf_file):
    """Extract text and split into chunks"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    all_text = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            all_text.append(text)
    full_text = "\n".join(all_text)
    chunks = chunk_text(full_text, chunk_size=800, overlap=100)
    return chunks

def find_relevant_chunks(chunks, query, top_k=3):
    """Simple keyword search to find relevant chunks"""
    query_terms = set(re.findall(r"\w+", query.lower()))
    scored_chunks = []
    for chunk in chunks:
        chunk_terms = set(re.findall(r"\w+", chunk.lower()))
        score = len(query_terms.intersection(chunk_terms))
        scored_chunks.append((score, chunk))
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored_chunks[:top_k]]

# --- PDF UPLOAD ---

uploaded_pdf = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_pdf and GROQ_API_KEY:
    with st.spinner("Extracting and chunking PDF content..."):
        chunks = extract_pdf(uploaded_pdf)
    st.success(f"PDF processed into {len(chunks)} chunks! You can now ask questions.")

    # Chat interface
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask a question about your PDF:")

    if st.button("Ask") and user_question:
        with st.spinner("Searching and getting answer from Groq..."):
            relevant_chunks = find_relevant_chunks(chunks, user_question, top_k=3)
            context = "\n\n".join(relevant_chunks)
            answer = ask_groq(user_question, context)
        st.session_state.chat_history.append((user_question, answer))

    # Display chat history
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**🤖 Answer:** {a}")
else:
    st.info("Please upload a PDF and enter your Groq API key to begin.")
