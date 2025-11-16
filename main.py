from fastapi import FastAPI , UploadFile, File , HTTPException 
from fastapi.responses import JSONResponse
from pydantic import Field 
import os
import tempfile
import shutil
from pathlib import Path

from core.config import get_settings
from langchain_groq import ChatGroq

from src.summarizer_pipeline import SummarizerPipeline
from rag.rag_pipeline import RagPipeline

from schema.request_model import RAGInput
from schema.response_model import RAGResponse, RAGSource

settings = get_settings()

MODEL_VERSION = "1.0.0"


llm = ChatGroq(model = "llama-3.3-70b-versatile" , 
               api_key = settings.GROQ_API_KEY)

rag_pipeline = RagPipeline(llm)


app = FastAPI(
     title = "Legal Document Summarizer and RAG API",
     description="API for Summarizing leagal files along with RAG",
     version = MODEL_VERSION
 )
 


# ------------
# HOME PAGE
# ------------

@app.get("/")
def read_root() :
    return {
        "LawLens : A voice enab,ed legal document summarizer with RAG"
    }


# ------------
# HEALTH CHECK
# ------------

@app.get("/health")
def read_health() :
    return {
        "status" : "OK" , "version" : MODEL_VERSION , "api" : "up and running" , "endpoints" : ["/summarize" , "/rag/ask"]
    }



# ------------
# SUMMARIZER
# ------------

@app.post("/summarize") 
async def summarize_text(
    file : UploadFile = File(...) ,
    language : str = "English" ,
    tts : bool = False
) :
    
    tmp_path = None
    

    try :
        '''Validate extension using config file'''
        ext = "." + file.filename.split(".")[-1].lower()

        if ext not in settings.ALLOWED_EXTENSIONS :
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        size = file.size
        if size > settings.MAX_FILE_SIZE:
            raise HTTPException(400, "File too large.")
        
        
        if language not in settings.SUPPORTED_LANGUAGES :
            raise HTTPException(status_code=400, detail="Invalid language")
        

 
        '''Save uploaded file temporarily. The UplaodFile is an object by FASTAPI but has no real path. The docloader cant read from that. So we create real file temporarily'''
        suffix = os.path.splitext(file.filename)[1]  # get .pdf / .txt / .docx

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            '''copies file stream to new real file'''
            shutil.copyfileobj(file.file, tmp)


        '''Summarizer Pipeline'''
        pipeline = SummarizerPipeline(llm , language)

        result = pipeline.run(tmp_path , tts)

        if tts :
            summary_text , audio_bytes = result

            return {
                "summary" : summary_text , 
                "audio_bytes" : audio_bytes.hex()   # send audio as hex string
            }
        
        return {
            "summary" : result
        }
        

    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))
    
    finally :
        if os.path.exists(tmp_path):
            os.remove(tmp_path)




#-------------------------------------
# RAG UPLOAD DOCUMENTS (INDEX BUILDER)
#-------------------------------------

@app.post("/rag/index")
async def build_index(file : UploadFile = File(...)) :
    '''Upload a document (PDF, TXT, DOCX) and ingest it.
    Build vector store and retriever for querying.'''

    try :

        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in settings.ALLOWED_EXTENSIONS :
            raise HTTPException(status_code=400, detail = f"Invalid file type : {file_ext}. Allowed extensions : {settings.ALLOWED_EXTENSIONS}")
        
        with tempfile.NamedTemporaryFile(delete=False , suffix=file_ext) as tmp:
            file_path = tmp.name
            shutil.copyfileobj(file.file, tmp)

            result = rag_pipeline.ingest_documents(file_path)
            os.remove(file_path)

            return JSONResponse(
                content = {
                    "status" : result['status'] ,
                    "message" : result['message'] , 
                    "chunks" : result['chunks'] ,
                   
                }
            )
            
        

    except Exception as e :
        raise HTTPException(status_code=500, detail=str(e))
    


#---------------------
# RAG ASK QUESTION
#---------------------


@app.post("/rag/ask" , response_model = RAGResponse)
async def ask(request : RAGInput) :
    '''Ask a question and get RAG-enhanced answer. request is an object of Pydantic class RAGInput'''
    query = request.query
    language = request.language

    try :
        if not query :
            raise HTTPException(status_code=400, detail="Query can't be empty. Please provide a query")
        
        if language not in settings.SUPPORTED_LANGUAGES :
            raise HTTPException(status_code=400, detail="Invalid language")
        
        if rag_pipeline.retriever is None :
            raise HTTPException(status_code=400, detail="Index not built. Please upload a document first.")


        result , retrieved_docs = rag_pipeline.ask_question(query , language)

        sources = [
        RAGSource(
            content=doc.page_content
        )
        for doc in retrieved_docs
    ] 
        
        return RAGResponse(
            answer = result , 
            sources = sources

        )

    except Exception as e :
        raise HTTPException(status_code=500, detail = f"Error processing query : {str(e)}")






















