from pydantic import BaseModel , Field
from typing import Optional 


class RAGInput(BaseModel) :
    '''
    Pydantic model for query validation
    '''

    query : str = Field(... , description = "The question to be asked")
    language : Optional[str] = Field(default = "English" , description = "The language of the question")

