from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
async def home():
   return {"message": "Hello World"}

@app.post("/students")
async def student_data(name:str=Body(...),
marks:int=Body(...)):
   return {"name":name,"marks": marks}

