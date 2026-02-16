# 📄 Smart Document Analyzer (OCR + Summary + Q&A)

An AI-powered web app to upload documents (PDFs/images), extract text (OCR), generate concise summaries, and answer questions based on the document content. Built with **Streamlit** and **Hugging Face Transformers**.

🔗 **Live Demo:**  
https://smart-doc-analyzer-orjhyexeamyoydwnuaufdj.streamlit.app/

---

## ✨ Features

- 📥 Upload **PDFs** and **Images**
- 🔍 Extract text from documents  
  - PDFs: text extraction  
  - Images: OCR (Tesseract – works locally)
- 🧠 Generate **concise summaries** of documents
- ❓ Ask **questions** and get answers grounded in the document
- ⚡ Fast and simple UI with Streamlit
- ☁️ Cloud-safe deployment (PDFs supported on Streamlit Cloud)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **NLP Models:** Hugging Face Transformers  
  - FLAN-T5 (text generation for summaries)  
  - RoBERTa/DistilBERT (question answering)  
- **OCR:** Tesseract (local)  
- **PDF Parsing:** pdfplumber  
- **Language:** Python

---

## ✅ Requirements & Conditions (Important)

Please note the following conditions to run this project smoothly:

- **Python:** 3.9+ recommended  
- **Internet connection:** Required on first run to download AI models  
- **RAM:** At least 4GB (8GB recommended for faster performance)  
- **Platform differences:**
  - **Local (Windows/Mac/Linux):**
    - PDF extraction works
    - Image OCR works (requires Tesseract installed locally)
  - **Streamlit Cloud:**
    - PDF extraction works
    - ❌ Image OCR is **not supported** (system OCR tools are not available on cloud)
- **Document quality:**
  - OCR accuracy depends on image clarity (handwritten/math may produce noisy text)
  - Scanned or blurry images may reduce accuracy
- **Model limitations:**
  - Summaries and answers are AI-generated and may not be 100% accurate
  - Long documents are truncated/chunked for performance
  - Very complex tables or formulas may not be parsed perfectly

---

## 🚀 How It Works

1. Upload a document (PDF or image).  
2. The app extracts readable text.  
3. Click **Summarize** to get a short overview of the document.  
4. Ask questions like:
   - “What is this document about?”  
   - “What is the difference between TCP and UDP?”  
   - “What experience does this resume mention?”

The model uses the document text as **context**, so different files produce different answers.

---

## ▶️ Run Locally

### 1) Clone the repo
```bash
git clone https://github.com/tejasmnaidu/smart-doc-analyzer.git
cd smart-doc-analyzer

