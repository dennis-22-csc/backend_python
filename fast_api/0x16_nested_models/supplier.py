from pydantic import BaseModel

class Supplier(BaseModel):
   supplierID:int
   supplierName:str
