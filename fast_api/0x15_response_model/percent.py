from typing import List
from pydantic import BaseModel, Field

class Percent(BaseModel):
   id:int
   name :str = Field(None, title="name of student", max_length=10)
   percent_marks: float

