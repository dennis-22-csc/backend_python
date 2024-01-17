from pydantic import BaseModel
from supplier import Supplier

class Product(BaseModel):
   productID:int
   prodname:str
   price:int
   supp:Supplier
