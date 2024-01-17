from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def home():
   return {"message": "Hello World"}

@app.get("/hello/{name}")
async def hello(name):
   return {"name": name}

@app.get("/hello/{name}/{age}")
async def hello(name,age):
   return {"name": name, "age":age}
