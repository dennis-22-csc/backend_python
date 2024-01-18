import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String

class Client(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'api_clients'
        full_name = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        secret = Column(String(128), nullable=False)
    else:   
        full_name = ""
        password = ""
        email = ""
        secret = "" 
