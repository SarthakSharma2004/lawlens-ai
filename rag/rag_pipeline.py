from rag.retriever import RetrieverBuilder
from rag.vector_store import VectorStore
from langchain.schema import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from prompts import PromptManager
from langchain.text_splitter import RecursiveCharacterTextSplitter
class RagPipeline :
    '''
    Builds and runs the full RAG pipeline
    '''

    @staticmethod
    def build_pipeline(llm , documents : list[Document] , persist_dir : str = None) :
        '''Full RAG pipeline'''
        splitter = RecursiveCharacterTextSplitter(chunk_size = 400 , chunk_overlap = 80)

        chunks = splitter.split_documents(documents)

        ''' Build Vector Store (embeddings + storage)'''
        vectorstore = VectorStore.build_vector_store(chunks , persist_dir)

        ''' Build Retriever '''
        retriever = RetrieverBuilder.build_retriever(vectorstore)

        ''' Build Chain '''
        stuff_chain = create_stuff_documents_chain(llm = llm , prompt = PromptManager.get_rag_prompt())

        retriever_chain = create_retrieval_chain(stuff_chain , retriever)

        return retriever_chain
    
    @staticmethod
    def run_pipeline(llm , documents , query : str , language : str = "English") -> str :
        chain = RagPipeline.build_pipeline(llm , documents)

        result = chain.invoke({"input" : query , "language" : language})

        return result
