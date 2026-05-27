# YouTube RAG Chat 🎥

An AI powered YouTube Question Answering System built using **RAG (Retrieval Augmented Generation)**, **LangChain**, **ChromaDB**, **Groq LLM**, and **Streamlit**.

This application allows users to:

- Upload any YouTube video link with no barrier of language
- Extract transcripts automatically no manual contribution needed
- Translate non English videos into English
- Create vector embeddings
- Ask questions directly from the video content
- Download transcripts in original and English language

Built with scalable multiuser session support to prevent database overlap between users and also making the application safe for each and every user.

---

# Features 🚀

- YouTube Transcript Extraction
- Multi language Video Support
- Automatic English Translation
- RAG-based Question Answering
- Chroma Vector Database
- Groq LLM Integration
- Chat History Awareness
- Query Rewriting for Better Retrieval
- Downloadable Transcripts
- Multi user Session Isolation
- Interactive Streamlit UI

---

# Tech Stack 🛠️

## Frontend

- Streamlit

## Backend / AI

- LangChain
- Groq API
- ChromaDB
- HuggingFace Embeddings
- Llama 3.1 8B Instant

## Utilities

- youtube-transcript-api
- yt-dlp
- googletrans
- httpx

---

# Project Structure 📂

```bash
.
├── streamlit.py
├── data_inegstion.py
├── RAG_retriever.py
├── utilities.py
├── requirements.txt
└── README.md
```

---

# Installation ⚙️

## 1. Clone Repository

```bash
git clone https://github.com/your-username/youtube-rag-chat.git

cd youtube-rag-chat
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run The Application ▶️

```bash
streamlit run streamlit.py
```

---

# How It Works ⚡

## Step 1

User enters YouTube video URL.

## Step 2

Transcript is extracted using:

- `youtube-transcript-api`

## Step 3

If transcript is not in English:

- It gets translated using `googletrans`

## Step 4

Transcript is chunked using:

- `RecursiveCharacterTextSplitter`

## Step 5

Embeddings are generated using:

- `all-MiniLM-L6-v2`

## Step 6

Chunks are stored in:

- `ChromaDB Vector Database`

## Step 7

User asks questions.

## Step 8

RAG pipeline:

- Rewrites query
- Retrieves relevant chunks
- Sends context to Groq LLM
- Generates final response

---

# Multi-User Session Support 👥

Every user gets a unique session ID using UUID.

This ensures:

- Separate vector databases
- No chat overlap
- Safe concurrent usage
- Scalable deployment

---

# Example Features 📌

## Video Information

- Thumbnail
- Title
- Channel Name
- Views
- Duration
- Description

## Transcript Support

- Original Language Transcript
- English Transcript
- Downloadable `.txt` files

## AI Chat

- Context-aware conversation
- Retrieval-enhanced answers
- Smart query rewriting

---

# Models Used 🤖

| Component | Model |
|---|---|
| Embedding Model | all-MiniLM-L6-v2 |
| LLM | llama-3.1-8b-instant |
| Vector DB | ChromaDB |

---

# Requirements 📦

```txt
streamlit
youtube-transcript-api
yt-dlp
langchain
langchain-core
langchain-community
langchain-text-splitters
langchain-huggingface
langchain-chroma
langchain-groq
chromadb
sentence-transformers
transformers
torch
huggingface-hub
googletrans==4.0.0rc1
httpx
python-dotenv
```

---

# Author 👨‍💻

Made by **Kunsh Bhatia**

GitHub: https://github.com/kunshbhatia/Youtube-RAG

---

# Disclaimer ⚠️

This is an AI-powered system and may occasionally generate incorrect answers. Always verify important information independently.