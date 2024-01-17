from fastapi import FastAPI, Depends
from dependency import Dependency

app = FastAPI()

@app.get("/user/")
async def user(dep: Dependency = Depends(Dependency)):
   return dep
@app.get("/admin/")
async def admin(dep: Dependency = Depends(Dependency)):
   return dep 
