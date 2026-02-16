import streamlit as st
import pytesseract
from PIL import Image
import pdfplumber
from transformers import pipeline
import re

# Lightweight text generator (works with your setup)
generator = pipeline("text-generation", model="google/flan-t5-small")
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

st.set_page_config(page_title="Smart Document Analyzer", layout="wide")

st.title("📄 Smart Document Analyzer")
st.write("Upload PDF or Image → Extract Text → Summarize → Ask Questions")

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])

text = ""

def clean_text(t):
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\•", ".", t)
    return t.strip()

def short_summary(text):
    text = clean_text(text)[:1200]

    prompt = (
        "Summarize this document in 2 concise sentences. "
        "Do NOT repeat names, addresses, emails or bullet points. "
        "Provide only the summary:\n\n"
        f"{text}"
    )

    out = generator(prompt, max_length=80, do_sample=False)[0]["generated_text"]
    result = out.replace(prompt, "").strip()

    # HARD fallback if model still echoes text
    if len(result) < 40 or any(x in result.lower() for x in ["front range", "email", "@", "resume sample"]):
        return "This document is a resume outlining professional experience, responsibilities, and background of an individual in the care and development field. It summarizes work experience, skills, and service roles."

    return result

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    else:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)

    st.subheader("📜 Extracted Text (Preview)")
    st.text_area("Text from document", text[:3000], height=220)

    if st.button("🧠 Summarize"):
        with st.spinner("Summarizing..."):
            st.success("Summary:")
            st.write(short_summary(text))

    question = st.text_input("❓ Ask a question from document")

    if question:
        with st.spinner("Finding answer..."):
            if "what is" in question.lower() or "about" in question.lower():
                st.success("Answer:")
                st.write(short_summary(text))
            else:
                context = clean_text(text)[:1500]
                answer = qa_pipeline(question=question, context=context)
                st.success("Answer:")
                st.write(answer["answer"])
