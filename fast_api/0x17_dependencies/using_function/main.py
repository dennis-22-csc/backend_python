from fastapi import FastAPI, Depends

app = FastAPI()

async def dependency(id: str, name: str, age: int):
   return {"id": id, "name": name, "age": age}

@app.get("/user/")
async def user(dep: dict = Depends(dependency)):
   return dep

@app.get("/admin/")
async def admin(dep: dict = Depends(dependency)):
   return dep
