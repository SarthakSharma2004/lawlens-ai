from rag.retriever import RetrieverBuilder
from rag.vector_store import VectorStore
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from prompt_templates.prompts import PromptManager
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.language_models import BaseChatModel
from src.document_processor import DocumentProcessorFactory



class RagPipeline :
    '''
    Full orchestration:
    - Extract text
    - Build index
    - Ask question
    - Convert answer to speech (optional)
    '''

    def __init__(self , llm : BaseChatModel , chunk_size : int = 400 , chunk_overlap : int = 80) :

        self.llm = llm
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.prompt = PromptManager.get_rag_prompt()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size ,
            chunk_overlap = self.chunk_overlap
        )
        self.retriever = None # Store retriever (will be set during ingesting documents)


    def ingest_documents(self , file_path : str) :
        '''Process document and create vector store + retriever.
        Call this once when user uploads a document'''

        try : 
            docs = DocumentProcessorFactory.process(file_path)

            chunks = self.splitter.split_documents(docs)

            vectorstore = VectorStore.build_vector_store(chunks)

            self.retriever = RetrieverBuilder.build_retriever(vectorstore) # stored retriever

            return {
                "status": "success",
                "message": "Document ingested successfully , index built" ,
                "chunks": len(chunks)
            
            }
        
        except Exception as e:
            raise RuntimeError(f"Error ingesting document: {e}")
        
    
    def ask_question(self , query : str , language : str = "English") -> str :
        '''Ask a question and get RAG-enhanced answer.'''

        try : 

            if self.retriever is None :
                raise RuntimeError("Index not built , No documents ingested. Call ingest_documents() first.")
            
            retrieved_docs = self.retriever.get_relevant_documents(query)
        
            stuff_chain = create_stuff_documents_chain(
                llm = self.llm , prompt = self.prompt
            )

            retrieval_chain = create_retrieval_chain(
                self.retriever , 
                stuff_chain
            )

            response = retrieval_chain.invoke(
                {"input" : query , "language" : language}
            )

            return response['answer'] , retrieved_docs

        except Exception as e:
            raise RuntimeError(f"Error during question-answering: {e}")


        






