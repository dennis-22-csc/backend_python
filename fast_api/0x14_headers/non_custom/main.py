from typing import Optional
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/headers/")
async def read_header(accept_language: Optional[str] = Header(None)):
   return {"Accept-Language": accept_language} 
