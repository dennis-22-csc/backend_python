import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Integer

class AuthCode(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'auth_codes'
        code = Column(String(128), nullable=False)
        client_email = Column(String(128), nullable=False)
        expires_in = Column(Integer, nullable=False, default=0)
    else:
        code = ""
        client_email = ""
        expires_in = ""
