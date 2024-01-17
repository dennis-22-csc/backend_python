from typing import List
from pydantic import BaseModel

class Student(BaseModel):
   id: int
   name :str
   subjects: List[str] = []
