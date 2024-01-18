import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer

class AccessToken(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'access_tokens'
        access_token = Column(String(128), nullable=False)
        expires_in = Column(Integer, nullable=False, default=0)
    else:
        access_token = ""
        expires_in = ""
