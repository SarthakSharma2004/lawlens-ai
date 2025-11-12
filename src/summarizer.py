from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from abc import ABC , abstractmethod
from prompts import PromptManager



class DocumentAnalyser :
    """
    Analyzes a list of Document objects and determines
    the total text length and which summarization approach to use.
    """

    TOKEN_THRESHOLD = 8000
    CHARS_PER_TOKEN = 4

    @staticmethod
    def count_tokens(documents : list[Document]) -> int :
        """Estimates token count from documents"""

        total_chars = sum(len(doc.page_content) for doc in documents)
        estimated_tokens = (total_chars // DocumentAnalyser.CHARS_PER_TOKEN)
        return estimated_tokens

    @staticmethod
    def suggest_chain_type(documents : list[Document]) -> str :
        """Determines which summarization approach to use based on token count"""

        token_count = DocumentAnalyser.count_tokens(documents)
        if token_count > DocumentAnalyser.TOKEN_THRESHOLD :
            return "map_reduce"
        else :
            return "map_summarize"


class BaseSummarizer(ABC) :

    '''It provides common methods like document validation and splitting, 
    while enforcing that every child class implements its own `summarize()` method.
    '''
    def __init__(self , llm , chunk_size : int = 400 , chunk_overlap : int = 80) :
        self.llm = llm
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def validate_docs(self , documents : list[Document]) -> None :
        '''Checks if the incoming documents are valid.'''
        if not documents or len(documents) == 0 :
            raise ValueError("No documents provided for summarization.")
        
        
    def split_docs(self , documents : list[Document]) -> list[Document] :
        """Splits the incoming documents into smaller chunks."""
        self.validate_docs(documents)

        try : 
            splitter = RecursiveCharacterTextSplitter(
                chunk_size = self.chunk_size , 
                chunk_overlap = self.chunk_overlap
            )
            return splitter.split_documents(documents)
        except Exception as e:
            raise RuntimeError(f"Error splitting documents: {e}")
        
    @abstractmethod
    def summarize(self , documents : list[Document]) :
        """Each summarizer (MapReduce, Stuff, etc.) will implement this."""
        pass





class MapReduceSummarizer :
    '''
    Document summarizer using MapReduce chain strategy. 
    How MapReduce Works:
    1. MAP Phase: Document is split into chunks, each chunk is summarized separately
    2. REDUCE Phase: All chunk summaries are combined into one final summary
    '''
    def __init__(self , llm , chunk_size : int = 400 , chunk_overlap : int = 90) :
        self.llm = llm
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    
    def validate_docs(self, documents : list[Document]) -> None :
        '''Checks if the incoming documents are valid.'''
        
        if not documents or len(documents) == 0 :
            raise ValueError("No documents provided for summarization.")
        
        
    def split_docs(self , documents : list[Document]) -> list[Document] :
        """Splits the incoming documents into smaller chunks."""
        self.validate_docs(documents)

        try : 
            splitter = RecursiveCharacterTextSplitter(
                chunk_size = self.chunk_size , 
                chunk_overlap = self.chunk_overlap
            )
            return splitter.split_documents(documents)
        except Exception as e:
            raise RuntimeError(f"Error splitting document: {e}")
        
    def summarize(self , documents : list[Document]) :
  
        """Performs summarization using map-reduce chain."""
        chunks = self.split_docs(documents)

        map_prompt = PromptManager.get_map_prompt()
        reduce_prompt = PromptManager.get_reduce_prompt()

        try : 

            chain = load_summarize_chain(
                llm = self.llm , 
                chain_type = "map_reduce" ,
                map_prompt = map_prompt , 
                combine_prompt = reduce_prompt
            )

            summary = chain.invoke(chunks)

            if isinstance(summary , dict) :
                return summary['output_text']
            else :
                return str(summary)
        
        except Exception as e:
            raise RuntimeError(f"Error during summarization: {e}")



        






        

