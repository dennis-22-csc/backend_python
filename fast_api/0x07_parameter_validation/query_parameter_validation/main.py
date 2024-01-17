from fastapi import FastAPI, Query


app = FastAPI()

@app.get("/")
async def home():
   return {"message": "Hello World"}

@app.get("/hello")
async def hello(name:str=Query(min_length=3, max_length=10),age:int=Query(ge=18, le=35)):
   return {"name":name, "age":age}

