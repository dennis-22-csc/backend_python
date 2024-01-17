from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():
   return {"message": "Hello World"}

@app.get("/hello/{name}/{age}")
async def hello(name: str,age: int):
   return {"name":name, "age":age}

@app.get("/hello")
async def hello(name:str,age:int):
   return {"name":name, "age":age}

@app.get("/hello/{name}")
async def hello(name:str,age:int):
   return {"name":name, "age":age}
