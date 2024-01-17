from typing import List
from pydantic import BaseModel, constr

class Book(BaseModel):
   id: int
   title: str
   author:str
   publisher: str
   class Config:
      orm_mode = True

