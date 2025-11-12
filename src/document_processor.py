from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader

from abc import ABC, abstractmethod
from langchain_core.documents import Document

class DataProcessor(ABC) :
    def __init__(self , file_path : str) -> None :
        self.file_path = file_path

    @abstractmethod
    def extract_text(self) :
        """Extracts text and returns list of Document objects."""
        pass
        
        

class PDFProcessor(DataProcessor) :
    def extract_text(self) -> list[Document] :        
        try : 
            loader = PyPDFLoader(self.file_path)
            return loader.load()
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")
        
    
class TXTProcessor(DataProcessor) :
    def extract_text(self) -> list[Document] :
        try : 
            loader = TextLoader(self.file_path)
            return loader.load()
        except Exception as e:
            raise RuntimeError(f"Error reading TXT: {e}")
        
    
class DOCXProcessor(DataProcessor) :
    def extract_text(self) -> list[Document] :
        try : 
            loader = Docx2txtLoader(self.file_path)
            return loader.load()
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX: {e}")
        
    
class DocumentProcessorFactory :
    """
    Factory class responsible for selecting and executing the correct document processor
    based on the file extension (PDF, TXT, or DOCX).
    """

    @staticmethod
    def get_processor(file_path : str) :
        """
        Determines the appropriate processor class based on file extension
        and returns an instance of that processor.
        """
        if file_path.endswith(".pdf") :
            return PDFProcessor(file_path)
        elif file_path.endswith(".txt") :
            return TXTProcessor(file_path)
        elif file_path.endswith(".docx") :
            return DOCXProcessor(file_path)
        else :
            raise ValueError(f"Unsupported file format: {file_path}")
        
    @staticmethod
    def process(file_path : str) :
        """
        Automatically creates the correct processor
        and extracts text while handling any runtime errors.
        """
        try :
            processor = DocumentProcessorFactory.get_processor(file_path)
            docs = processor.extract_text()
            return docs

        except Exception as e:
            raise RuntimeError(f"Error processing document: {e}")



