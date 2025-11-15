from fastapi import FastAPI , UploadFile, File , HTTPException
from pydantic import Field
import os
import tempfile
import shutil

from core.config import get_settings
from langchain_groq import ChatGroq



from src.summarizer_pipeline import SummarizerPipeline


settings = get_settings()

MODEL_VERSION = "1.0.0"

PERSIST_DIR = "rag_storage"
os.makedirs(PERSIST_DIR , exist_ok = True)

llm = ChatGroq(model = "llama-3.3-70b-versatile" , 
               api_key = settings.GROQ_API_KEY)


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

















# settings = get_settings()

# MODEL_VERSION = "1.0.0"

# app = FastAPI(
#     title = "Legal Document Summarizer and RAG API",
#     description="API for Summarizing leagal files along with RAG",
#     version = MODEL_VERSION
# )


# def get_llm() :
#     llm = ChatGroq(
#         model = "llama-3.3-70b-versatile" , 
#         api_key = settings.GROQ_API_KEY
#     )

#     return llm



# # ---------------------------
# #  NORMAL LANDING PAGE
# # ---------------------------


# @app.get("/")
# def read_root() :
#     return {
#         "LawLens : A legal document summarizer with voice support and RAG"
#     }



# @app.get("/health")
# def read_health() :
#     return {
#         "status" : "OK" , 
#         "version" : MODEL_VERSION , 
#         "API" : "up and running" , 
#         "endpoints" : [
#             "/summarize" , 
#             "/rag/ask"
#         ]
#     }


# # ---------------------------
# #  SUMMARIZATION ENDPOINT
# # ---------------------------


# @app.post("/summarize" , response_model = SummaryResponse)
# async def summarize_text(file : UploadFile = File(...) , language : str = "English" , tts : bool = False) :
    
#     try :
#         '''Save uploaded file temporarily'''
#         suffix = os.path.splitext(file.filename)[1]  # get .pdf / .txt / .docx

#         with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             tmp_path = tmp.name
#             shutil.copyfileobj(file.file, tmp)

#             pipeline = SummarizerPipeline(llm = get_llm() , language = language)

#             result = pipeline.run(file_path = tmp_path , tts = tts)

#         # 4. Formatting output
#         if tts:
#             summary_text, audio_bytes = result

#             return {
#                 "summary": summary_text,
#                 "audio_bytes": audio_bytes.hex()   # send audio as hex string
#             }
#         else:
#             return {"summary": result}

        
#     except Exception as e :
#         raise HTTPException(status_code=400, detail=str(e))
    
    

# # ---------------------------
# #  RAG ENDPOINT
# # ---------------------------


# @app.post("/rag/ask" , response_model = RAGResponse)
# async def rag_ask(file : UploadFile = File(...) , query : str = "" , language : str = "English") :
    
#         '''Save uploaded file temporarily'''
#         if query == "" :
#             raise HTTPException(status_code=400, detail="Please provide a query")
        
#         try:
#             # Save uploaded file
#             suffix = os.path.splitext(file.filename)[1]  # get .pdf / .txt / .docx

#             with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#                 tmp_path = tmp.name
#                 shutil.copyfileobj(file.file, tmp)

            

#             # Create pipeline
#             rag_pipeline = RagPipeline(llm=get_llm())

#             # Build index from uploaded file
#             rag_pipeline.build_index(tmp_path)

#             # Then ask question
#             answer = rag_pipeline.ask(query, language)

#             return {"answer": answer}

#         except Exception as e:
#             raise HTTPException(status_code=400, detail=str(e))

    