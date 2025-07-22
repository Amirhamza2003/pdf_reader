import streamlit as st
import fitz  # PyMuPDF
import os
import json
import requests
from PIL import Image

# Streamlit page config
st.set_page_config(page_title="PDF Q&A Chatbot", page_icon="📄", layout="centered")

st.title(" PDF Q&A Chatbot")
st.markdown(
    """
    Upload a PDF, extract its content, and ask questions about it using Groq's Llama 3 model.
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
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception:
        return "❌ Error: Could not get a response from Groq API."

def image_to_text_groq(image_path):
    return f"[Image OCR simulation: You uploaded {os.path.basename(image_path)}]"

def extract_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text_data = []
    image_captions = []

    for i, page in enumerate(doc):
        text = page.get_text()
        text_data.append(text)

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_caption = image_to_text_groq(f"page_{i+1}_img_{img_index+1}.{image_ext}")
            image_captions.append(image_caption)

    combined_text = "\n".join(text_data + image_captions)
    return combined_text

# --- PDF UPLOAD ---
uploaded_pdf = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_pdf and GROQ_API_KEY:
    with st.spinner("Extracting PDF content..."):
        context = extract_pdf(uploaded_pdf)
    st.success("PDF processed! You can now ask questions about it.")

    # Chat interface
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask a question about your PDF:")

    if st.button("Ask") and user_question:
        with st.spinner("Getting answer from Groq..."):
            answer = ask_groq(user_question, context)
        st.session_state.chat_history.append((user_question, answer))

    # Display chat history
    for q, a in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**🤖 Answer:** {a}")
else:
    st.info("Please upload a PDF and enter your Groq API key to begin.")