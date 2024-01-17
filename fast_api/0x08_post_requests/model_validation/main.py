from fastapi import FastAPI
from student import Student

app = FastAPI()

@app.get("/")
async def home():
   return {"message": "Hello World"}

@app.post("/students/")
async def student_data(s1: Student):
   return s1
