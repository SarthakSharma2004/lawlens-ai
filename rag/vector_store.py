from langchain.vectorstores import Chroma
from langchain.schema import Document
from rag.embedder import Embedder
class VectorStore :
    '''
    Builds a Chroma vector store from document chunks.
    calls the embedder class (gemini embeddings) to create embeddings.
    '''
    @staticmethod
    def build_vector_store(chunks : list[Document] , persist_dir : str = None) :
        '''
        Creates and returns a Chroma vector store containing embeddings
        for the given document chunks. 
        '''
        
        try : 
            embedder = Embedder.get_embedder()
            vectorstore =  Chroma.from_documents(
                documents = chunks ,
                embedding = embedder , 
                persist_directory = persist_dir
            ) 

            return vectorstore
        
        except Exception as e:
            raise RuntimeError(f"Error creating vector store: {e}")

            