from fastapi import FastAPI, Path


app = FastAPI()

@app.get("/")
async def home():
   return {"message": "Hello World"}

#Path validation minimun and max length for path name
@app.get("/hello1/{name}/{age}")
async def hello1(name:str=Path(min_length=3, max_length=10),age:int=None):
   return {"name":name, "age":age}

#Path validation age must not be greater than 120, age must be less than or equal to 120
@app.get("/hello2/{name}/{age}")
async def hello2(name:str=Path(min_length=3, max_length=10),age:int=Path(le=120)):
   return {"name":name, "age":age}

#Path validation age must not be less than 18, age must be greater than or equal to 18
@app.get("/hello3/{name}/{age}")
async def hello3(name:str=Path(min_length=3, max_length=10),age:int=Path(ge=18)):
   return {"name":name, "age":age}

#Path validation age must be between 18 and 35, age must be greater than or equal to 18, age must be less than or equal to 35
@app.get("/hello4/{name}/{age}")
async def hello4(name:str=Path(min_length=3, max_length=10),age:int=Path(ge=18, le=35)):
   return {"name":name, "age":age}

#Path validation age must be greater than 18
@app.get("/hello5/{name}/{age}")
async def hello5(name:str=Path(min_length=3, max_length=10),age:int=Path(gt=18)):
   return {"name":name, "age":age}

#Path validation age must be less than 35
@app.get("/hello6/{name}/{age}")
async def hello6(name:str=Path(min_length=3, max_length=10),age:int=Path(lt=35)):
   return {"name":name, "age":age}
