from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/response_headers/")
def set_response_headers():
   content = {"message": "Hello World"}
   headers = {"X-Web-Framework": "FastAPI", "Content-Language": "en-US"}
   return JSONResponse(content=content, headers=headers)
