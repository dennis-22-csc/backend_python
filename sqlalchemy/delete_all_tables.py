"""
This module deletes all tables in a database using SQLAlchemy.

It includes functionality for deleting tables in the database based on the SQLAlchemy Base model.

"""
from config import engine
from models import Base

# Deleting all tables in the database
Base.metadata.drop_all(engine)
