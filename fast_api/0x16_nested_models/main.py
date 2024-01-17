from fastapi import FastAPI
from customer import Customer

app = FastAPI()

@app.post('/invoice')
async def getInvoice(customer:Customer):
   return customer
