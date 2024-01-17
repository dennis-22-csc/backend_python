from fastapi import FastAPI
from student import Student

app = FastAPI()

@app.get("/")
async def home():
   return {"message": "Hello World"}

@app.post("/students/{college}")
async def student_data(college:str, age:int, student:Student):
   retval={"college":college, "age":age, **student.dict()}
   return retval
