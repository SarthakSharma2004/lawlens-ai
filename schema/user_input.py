from pydantic import BaseModel , Field
from typing import Optional 

class SummarizeInput(BaseModel):
    language : str = Field(default=["English"] , description = " Language you want the summary in")
    tts : bool = Field(default=False , description = " Whether to convert summary to audio or not")

class RAGInput(BaseModel) :
    question : str = Field(default = "" , description=" The question you want to ask")
    language : str = Field(default=["English"] , description = " Language you want the answer in")


