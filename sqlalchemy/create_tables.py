"""
This module initializes and creates database tables using SQLAlchemy.

It includes functionality for creating tables in the database based on the SQLAlchemy Base model.

"""
from config import engine
from models import Base

# Create tables in the database
Base.metadata.create_all(engine)
