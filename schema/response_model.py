from pydantic import BaseModel , Field 
from typing import Optional 

class SummaryResponse(BaseModel):
    summary : str = Field(... , description = "The summary of the document")
    audio_hex : Optional[str] = Field(default=None , description = " The audio of the summary in hex format")

class RAGResponse(BaseModel):
    answer : str = Field(... , description = "The answer to the question")
