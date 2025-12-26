<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-Framework-green"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS-EC2-orange?logo=amazonaws&logoColor=white"/>
  <br/>
  <img src="https://img.shields.io/badge/LLM-Groq_LLaMA--3-black"/>
  <img src="https://img.shields.io/badge/Gemini-Embeddings_+_TTS-blueviolet"/>
  <img src="https://img.shields.io/badge/VectorDB-ChromaDB-yellowgreen"/>
  <img src="https://img.shields.io/badge/LangSmith-Tracing_&_Observability-purple"/>
  <br/>
  <img src="https://img.shields.io/badge/Task-Document_Summarization-success"/>
  <img src="https://img.shields.io/badge/LangChain-Stuff_Chain-lightgrey"/>
  <img src="https://img.shields.io/badge/LangChain-Map--Reduce_Chain-lightgrey"/>
</p>


---

<h1 align="center">🤖⚖️ LawLens.ai </h1>

<h3 align="center">AI-Powered Legal Document Summarization & Intelligent Q&A System</h3>



---



## 🚀 Live Demo

[![Streamlit Live Demo](https://img.shields.io/badge/Streamlit-Live_Demo-FF4B4B?logo=streamlit&logoColor=white)](https://lawlens-ai.streamlit.app)


## 📦 Docker Image (Pull image from Docker Hub)

[![Docker Hub](https://img.shields.io/badge/Docker_Hub-lawlens--backend-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/isarthak24/lawlens-backend/general)



---



## ⭐ Overview

LawLens.ai is an end-to-end AI-powered system that simplifies complex legal documents using intelligent LLM-driven summarization and context-aware question answering supported by structured prompt engineering and adaptive processing pipelines.

The platform supports summarization in the user’s **preferred language** and provides an optional **audio playback** feature, enabling users to listen to generated summaries in their chosen language for improved accessibility.

To ensure optimal performance, LawLens.ai dynamically adapts its **summarization strategy based on document length**, automatically switching between **Stuff and Map-Reduce pipelines** to reduce inference latency by approximately **45%**. The system leverages LLaMA 3 via Groq for ultra-fast inference, Gemini embeddings for semantic retrieval, and a vector-based retrieval layer to deliver precise and reliable legal Q&A.


➡️ The system is powered by:

- LLaMA-3 (Groq Inference Engine) for ultra-fast summarization

- Gemini-TTS for natural audio generation

- gemini embedding model for Q&A module

- LangChain + LangSmith for orchestration and full pipeline tracing

- FastAPI for backend

- Docker for containerization

- AWS EC2 for deployment


---


## ✨ Key Features

- ⚡ **Adaptive Summarization Pipelines**
Dynamically switches between Stuff and Map-Reduce strategies based on document length, achieving ~45% reduction in inference latency.