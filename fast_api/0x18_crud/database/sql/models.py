from config import Base
from sqlalchemy import Column, Integer, String

class Books(Base):
   __tablename__ = 'book'
   id = Column(Integer, primary_key=True, nullable=False)
   title = Column(String(50), unique=True)
   author = Column(String(50))
   publisher = Column(String(50))
