from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from user import User 

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.post("/hello1/", response_class=HTMLResponse)
async def hello1(request: Request, user: User):
   return templates.TemplateResponse("hello.html", {"request": request, "user":user})

@app.post("/hello2/", response_class=HTMLResponse)
async def hello2(request: Request):
    return templates.TemplateResponse("hello.html", {"request": request, "user":None})

@app.get("/", response_class=HTMLResponse)
async def order_item(request: Request):
    return templates.TemplateResponse("product.html", {"request": request, "items": ["Phone", "Bag"]})
