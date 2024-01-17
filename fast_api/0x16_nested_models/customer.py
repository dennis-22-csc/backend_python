from pydantic import BaseModel
from typing import Tuple
from product import Product

class Customer(BaseModel):
   custID:int
   custname:str
   prod:Tuple[Product]
