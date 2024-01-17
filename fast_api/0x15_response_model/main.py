from fastapi import FastAPI
from student import Student
from percent import Percent

app = FastAPI()

@app.post("/marks", response_model=Percent)
async def get_percent(student:Student):
   student.percent_marks=sum(student.marks)/2
   return student
