from fastapi import FastAPI, Depends, HTTPException
from dependency import Dependency

app = FastAPI()

async def validate(dep: Dependency = Depends(Dependency)):
   if dep.age > 18:
      raise HTTPException(status_code=400, detail="You are not eligible")

@app.get("/user/", dependencies=[Depends(validate)])
async def user():
   return {"message": "You are eligible"}
