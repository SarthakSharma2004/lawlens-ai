from pydantic import BaseModel , Field 
from typing import Optional , List

class SummaryResponse(BaseModel):
    '''Pydantic model for summary response'''
    summary : str = Field(... , description = "The summary of the document")
    audio_hex : Optional[str] = Field(default=None , description = " The audio of the summary in hex format")




class RAGSource(BaseModel):
    '''Pydantic model to give retrieved chunks'''
    content : str = Field(... , description = "Retrieved context chunks")
   


class RAGResponse(BaseModel):
    '''Pydantic model for RAG response'''
    answer : str = Field(... , description = "The answer to the question")
    sources : Optional[List[RAGSource]] = Field(default=None , description = "Optional list of retrieved chunks used to generate the answer")

