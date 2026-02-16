import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import io
import os
from transformers import pipeline

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Smart Document Analyzer", layout="wide")

st.title("📄 Smart Document Analyzer")
st.caption("Upload PDF or Image → Extract Text → Summarize → Ask Questions")

# -------------------------
# Tesseract Path (Windows)
# -------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------------------------
# Load models safely
# -------------------------
@st.cache_resource
def load_models():
    summarizer = pipeline("text-generation", model="google/flan-t5-small")
    qa = pipeline("question-answering", model="deepset/roberta-base-squad2")
    return summarizer, qa

summarizer, qa_pipeline = load_models()

# -------------------------
# File uploader
# -------------------------
uploaded_file = st.file_uploader(
    "Upload PDF or Image",
    type=["pdf", "png", "jpg", "jpeg"]
)

extracted_text = ""

# -------------------------
# Extract text
# -------------------------
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"

    else:
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.image_to_string(image)

# -------------------------
# Display extracted text
# -------------------------
if extracted_text.strip():
    st.subheader("📜 Extracted Text (Preview)")
    st.text_area("Text from document", extracted_text, height=250)

# -------------------------
# Summarize
# -------------------------
summary_text = ""
if extracted_text.strip():
    if st.button("🧠 Summarize"):
        with st.spinner("Summarizing..."):
            prompt = f"Summarize the following content clearly:\n\n{extracted_text[:3000]}"
            result = summarizer(prompt, max_new_tokens=120)
            summary_text = result[0]["generated_text"]

        st.subheader("✅ Summary")
        st.success(summary_text)

# -------------------------
# Ask Questions
# -------------------------
if extracted_text.strip():
    st.subheader("❓ Ask a question from document")
    question = st.text_input("Enter your question:")

    if question:
        with st.spinner("Finding answer..."):
            answer = qa_pipeline(question=question, context=extracted_text[:4000])
            final_answer = answer.get("answer", "No clear answer found.")

        st.subheader("💡 Answer")
        st.success(final_answer)
