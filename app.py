import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
import os
from transformers import pipeline

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Smart Document Analyzer", layout="wide")

st.title("📄 Smart Document Analyzer")
st.caption("Upload PDF or Image → Extract Text → Summarize → Ask Questions")

# -------------------------
# Detect Streamlit Cloud
# -------------------------
def is_streamlit_cloud():
    return os.environ.get("STREAMLIT_SERVER_HEADLESS") == "true"

# -------------------------
# Tesseract Path (Local Windows only)
# -------------------------
if not is_streamlit_cloud():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------------------------
# Load models (cached)
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
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

    elif uploaded_file.type.startswith("image"):
        if is_streamlit_cloud():
            st.error("❌ Image OCR is not supported on Streamlit Cloud. Please upload a PDF or run locally for image OCR.")
            st.stop()
        else:
            image = Image.open(uploaded_file)
            extracted_text = pytesseract.image_to_string(image)

# -------------------------
# Display extracted text
# -------------------------
if extracted_text.strip():
    st.subheader("📜 Extracted Text (Preview)")
    st.text_area("Text from document", extracted_text[:4000], height=250)

# -------------------------
# Summarize
# -------------------------
if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""

if extracted_text.strip():
    if st.button("🧠 Summarize"):
        with st.spinner("Summarizing..."):
            prompt = f"Summarize the following content clearly:\n\n{extracted_text[:3000]}"
            result = summarizer(prompt, max_new_tokens=120)
            st.session_state.summary_text = result[0]["generated_text"].strip()

    if st.session_state.summary_text:
        st.subheader("✅ Summary")
        st.success(st.session_state.summary_text)


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
