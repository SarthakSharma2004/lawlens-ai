from langchain_google_genai import GoogleGenerativeAIEmbeddings
from core.config import get_settings

class Embedder:
    """
    Loads the embedding model used for the RAG pipeline.
    """
    settings = get_settings()
    @staticmethod 
    def get_embedder() :
        
        return GoogleGenerativeAIEmbeddings(
            model = "gemini-embedding-001" , 
            google_api_key = Embedder.settings.GOOGLE_API_KEY
    )
        
