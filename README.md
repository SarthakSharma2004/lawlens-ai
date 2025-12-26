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

- gemini embedding model & ChromaDB for Q&A module

- LangChain + LangSmith for orchestration and full pipeline tracing

- FastAPI for backend

- Docker for containerization

- AWS EC2 for deployment


---


## ✨ Key Features

- **🧠 Intelligent Legal Document Summarization**
Helps users quickly understand lengthy legal contracts, agreements, and  documents by converting complex legal text into clear, concise summaries while preserving critical legal context.

- **⚡ Adaptive Summarization Pipelines**
Dynamically switches between Stuff and Map-Reduce strategies based on document length, achieving ~45% reduction in inference latency.

- **🌍 Multi-Language Support**
Generates summaries in the user’s preferred language, making legal content accessible to a broader audience.

- **🔊 Optional Audio Playback (Text-to-Speech)**
Enables speech-based playback of generated summaries in the selected language using *gemini-tts* for enhanced accessibility.

- **🔍 Context-Aware Document Q&A**
Adds an additional functionality to allow users to ask natural language questions over uploaded documents using **semantic retrieval** with embeddings and vector search utilising **ChromaDB**

- **📦 Scalable Backend**
Built with **FastAPI**, containerized using **Docker**, and deployed on **AWS** EC2 for scalable and reliable inference.

- **📊 End-to-End Observability**
Integrated LangSmith tracing to monitor prompts, LLM calls, latency, and failure points across the entire pipeline.

- **🖥️ Interactive Web Interface**
Clean and intuitive Streamlit UI enabling document upload, summarization, Q&A, and audio playback in a seamless workflow.


---


## 🛠️ Tech Stack

🔹 Core Language & Frameworks

- **🐍 Python** — Primary language for backend logic and AI pipelines

- **🔗 LangChain** — Orchestrating summarization pipelines (Stuff & Map-Reduce) and Q&A workflows

- **⚡ FastAPI** — High-performance REST API for LLM inference and service integration


🔹 LLMs & AI Models

- **🧠 LLaMA 3 (via Groq)** — Ultra-fast LLM inference for summarization and reasoning

- **🌐 Gemini** — Embeddings for semantic retrieval and TTS for audio playback


🔹 Retrieval & Storage

- 🧾 **ChromaDB** — Vector database for storing embeddings and enabling semantic document search

- 📁 **Document Chunking & Indexing** — Efficient handling of large legal documents

🔹 Frontend & User Experience

- **🖥️ Streamlit** — Interactive web interface for document upload, summarization, Q&A, and audio playback


🔹 Infrastructure & Deployment

- **📦 Docker** — Containerization for consistent builds and deployments

- **☁️ AWS EC2** — Cloud deployment for scalable and reliable inference services


🔹 Monitoring & Observability

- **📊 LangSmith** — End-to-end tracing, latency monitoring, and prompt-level observability


---


## 🛠️ Installation & Setup

Follow the steps below to set up LawLens.ai locally.

### 📦 Clone the Repository

```bash
git clone https://github.com/SarthakSharma2004/lawlens-ai.git
```

### 🔑 Environment Variables

```bash
HUGGINGFACEHUB_API_TOKEN=
GOOGLE_API_KEY=
GROQ_API_KEY=
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=
LANGCHAIN_API_KEY=
LANGCHAIN_TRACING_V2=
LANGCHAIN_PROJECT=
```

### 🚀 Install Requirements

```bash
pip install -r requirements.txt
```


### 🎨 Run Locally (Without Docker)

```bash
Run FastAPI:

uvicorn app.main:app --reload

Run Streamlit:

streamlit run frontend/app.py
```

### 🐳 Run with Docker

```bash
docker pull isarthak24/lawlens-backend
docker run -p 8000:8000 --env-file .env isarthak24/lawlens-backend
```


---



## 👨‍💻 Author
Sarthak Sharma

Data Science | Machine Learning | Deep Learning | NLP | GenAI

[![Email](https://img.shields.io/badge/Email-Gmail-D14836?logo=gmail&logoColor=white)](mailto:2sarthaksharma@gmail.com)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sarthak-sharma-860b22259)