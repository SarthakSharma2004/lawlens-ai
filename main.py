from fastapi import FastAPI , UploadFile, File , HTTPException
from pydantic import Field
import os
import tempfile
import shutil

from core.config import get_settings
from langchain_groq import ChatGroq

from src.summarizer_pipeline import SummarizerPipeline
from rag.rag_pipeline import RagPipeline

from schema.response_model import SummaryResponse , RAGResponse

settings = get_settings()

MODEL_VERSION = "1.0.0"

app = FastAPI(
    title = "Legal Document Summarizer and RAG API",
    description="API for Summarizing leagal files along with RAG",
    version = MODEL_VERSION
)


def get_llm() :
    llm = ChatGroq(
        model = "llama-3.3-70b-versatile" , 
        api_key = settings.GROQ_API_KEY
    )

    return llm



# ---------------------------
#  NORMAL LANDING PAGE
# ---------------------------


@app.get("/")
def read_root() :
    return {
        "LawLens : A legal document summarizer with voice support and RAG"
    }



@app.get("/health")
def read_health() :
    return {
        "status" : "OK" , 
        "version" : MODEL_VERSION , 
        "API" : "up and running" , 
        "endpoints" : [
            "/summarize" , 
            "/rag/ask"
        ]
    }


# ---------------------------
#  SUMMARIZATION ENDPOINT
# ---------------------------


@app.post("/summarize" , response_model = SummaryResponse)
async def summarize_text(file : UploadFile = File(...) , language : str = "English" , tts : bool = False) :
    
    try :
        '''Save uploaded file temporarily'''
        suffix = os.path.splitext(file.filename)[1]  # get .pdf / .txt / .docx

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            shutil.copyfileobj(file.file, tmp)

            pipeline = SummarizerPipeline(llm = get_llm() , language = language)

            result = pipeline.run(file_path = tmp_path , tts = tts)

        # 4. Formatting output
        if tts:
            summary_text, audio_bytes = result

            return {
                "summary": summary_text,
                "audio_bytes": audio_bytes.hex()   # send audio as hex string
            }
        else:
            return {"summary": result}

        
    except Exception as e :
        raise HTTPException(status_code=400, detail=str(e))
    
    

# ---------------------------
#  RAG ENDPOINT
# ---------------------------


@app.post("/rag/ask" , response_model = RAGResponse)
async def rag_ask(file : UploadFile = File(...) , query : str = "" , language : str = "English") :
    
        '''Save uploaded file temporarily'''
        if query == "" :
            raise HTTPException(status_code=400, detail="Please provide a query")
        
        try:
            # Save uploaded file
            suffix = os.path.splitext(file.filename)[1]  # get .pdf / .txt / .docx

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp_path = tmp.name
                shutil.copyfileobj(file.file, tmp)

            

            # Create pipeline
            rag_pipeline = RagPipeline(llm=get_llm())

            # Build index from uploaded file
            rag_pipeline.build_index(tmp_path)

            # Then ask question
            answer = rag_pipeline.ask(query, language)

            return {"answer": answer}

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    