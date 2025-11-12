from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
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
            return "stuff"


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




class StuffSummariser(BaseSummarizer) :
    '''
    Summarizer class for smaller documents using the 'stuff' chain type.
    '''
    def summarize(self , documents : list[Document] , language : str = "English") -> str:
        """Summarizes the given documents using the 'stuff' approach."""
        self.validate_docs(documents)

        try : 

            chain = load_summarize_chain(
                llm = self.llm ,
                chain_type = "stuff" ,
                prompt = PromptManager.get_stuff_prompt()
            )

            summary = chain.invoke({
                    "text" : documents ,
                    "language" : language
            })

            if isinstance(summary , dict) and "output_text" in summary :
                return summary["output_text"]
            
            else :
                return str(summary)
            
        except Exception as e:
            raise RuntimeError(f"Error during summarization using stuff chain : {e}")





class MapReduceSummarizer(BaseSummarizer) :
    '''
    Document summarizer using MapReduce chain strategy. 
    How MapReduce Works:
    1. MAP Phase: Document is split into chunks, each chunk is summarized separately
    2. REDUCE Phase: All chunk summaries are combined into one final summary
    '''

    def summarize(self, documents : list[Document]) -> str :

        chunks = self.split_docs(documents)

        try : 

            chain = load_summarize_chain(
                llm = self.llm , 
                chain_type = "map_reduce" , 
                map_prompt = PromptManager.get_map_prompt() ,
                combine_prompt = PromptManager.get_reduce_prompt()
            )

            summary = chain.invoke({"text" : chunks})

            if isinstance(summary , dict) and "output_text" in summary :
                return summary["output_text"]
            else :
                return str(summary)
            
        except Exception as e:
            raise RuntimeError(f"Error during summarization using map_reduce chain : {e}")


        






        

