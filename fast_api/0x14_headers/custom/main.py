from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/custom_header/")
def set_custom_headers():
   content = {"message": "Hello World"}
   header = {"X-Web-Framework": "FastAPI"}
   return JSONResponse(content=content, headers=header)
