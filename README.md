</p> <p align="center"> <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" /> <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" /> <img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit" /> <img src="https://img.shields.io/badge/LangChain-Orchestration-1F68D0?logo=chainlink" /> <img src="https://img.shields.io/badge/LangSmith-Tracing-orange?logo=logstash" /> <img src="https://img.shields.io/badge/Groq-LLaMA_3_Inference-6E00FF?logo=groq" /> <img src="https://img.shields.io/badge/Gemini-Embeddings_+_TTS-4285F4?logo=google" /> <img src=\"https://img.shields.io/badge/RAG-Enabled-purple\" /> <img src=\"https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker\" /> <img src=\"https://img.shields.io/badge/AWS-EC2 Deployment-FF9900?logo=amazonaws\" /> <img src=\"https://img.shields.io/badge/Pydantic-Validation-0984e3?logo=pydantic\" /> </p>

---

# LawLens.ai – AI-Powered Legal Document Summarization & Q&A System

<p align="center">

🚀 LLaMA-3 (Groq) • Gemini-TTS • RAG • LangChain • FastAPI • Streamlit • Docker • AWS

---

### 🌐 Live Demo

- https://lawlens-ai.streamlit.app

---

## ⭐ Overview

LawLens.ai is an end-to-end AI-driven legal document understanding system designed to convert complex contracts into clear, concise summaries.
It supports multilingual summarization, natural speech playback, and intelligent Q&A using RAG — all deployed with a production-grade architecture.

The system is powered by:

- LLaMA-3 (Groq Inference Engine) for ultra-fast summarization

- Gemini-TTS for natural audio generation

- Gemini Embeddings for retrieval-augmented Q&A

- LangChain + LangSmith for orchestration and full pipeline tracing

Backend is built with FastAPI + Docker, deployed on AWS EC2.
Frontend is an interactive Streamlit app, hosted on Streamlit Cloud.


---


## ✨ Key Features

### 📄 Multilingual Summarization

Summarizes legal documents (PDF, DOCX, TXT) in any supported language using a dynamic summarization pipeline, switching between Stuff and Map Reduce Summarization techniques
for maintaining efficiency as well as high inference speed. 



### 🔊 Natural AI Text-to-Speech

Generate clean, natural audio using Gemini-2.5-Flash-TTS for hands-free summary playback.

---

### 🧠 RAG-Based Question Answering

Ask detailed questions about the uploaded contract.
Gemini embeddings + vector retrieval give context-aware, grounded answers.

---

### ⚡ Ultra-Fast LLM Inference

Powered by Groq, enabling real-time summarization with LLaMA-3 models.

---

### 📊 Complete Observability with LangSmith

Trace:

- Retrieval quality

- LLM calls

- Prompt flows

- Latency

- Fully integrated for production-grade debugging & monitoring. 

---

### 🧩 Clean, Scalable Architecture

- FastAPI backend

- Streamlit frontend

- Dockerized deployment

- Environment-driven config using Pydantic Settings

- Modular code structure


---


### 🏗️ Architecture Overview

                ┌──────────────────┐
                │   Streamlit UI   │
                └─────────┬────────┘
                          │
                    User Uploads
                          │
                ┌─────────▼─────────┐
                │    FastAPI API    │
                └─────────┬─────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
   Summarization     Text-to-Speech     RAG Retrieval
      (Groq)            (Gemini)        (Embeddings + DB)


### 🔧 Tech Stack

- FastAPI

- Python

- LangChain

- LangSmith

- Groq SDK (LLaMA-3 Inference)

- Gemini API (TTS + Embeddings)

- Pydantic 

- Streamlit

- Docker

- AWS EC2 Deployment

- Streamlit Cloud Hosting
