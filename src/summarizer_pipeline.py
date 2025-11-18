from src.document_processor import DocumentProcessorFactory
from src.summarizer import summarize_document
from src.speech import TextToSpeech
from langchain_core.language_models import BaseChatModel



class SummarizerPipeline :
    """
    Full orchestration:
    - Extract text
    - Summarize
    - Convert summary to speech (optional)
    """
    def __init__(self , llm : BaseChatModel , language : str = "English") :
        self.llm = llm
        self.language = language

    def run(self , file_path : str , tts : bool = False) :
        '''Runs complete pipeline.
        and returns summary_text OR (summary and audio_bytes)
        '''

        try :
            '''load and extract the text'''
            docs = DocumentProcessorFactory.process(file_path)

            '''summarize the text'''
            summary_text = summarize_document(llm = self.llm , documents = docs , language = self.language)

            '''convert summary to speech'''
            if tts :
                audio_bytes = TextToSpeech.text_to_speech(summary_text , language = self.language)
                return summary_text , audio_bytes
            
          
            return summary_text
        
        except Exception as e :
            raise RuntimeError(f"Error running pipeline: {e}")

