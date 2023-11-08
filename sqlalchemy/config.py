"""

This module provides SQLAlchemy utilities for working with a MYSQL database.

It includes functionality for creating an SQLAlchemy engine, defining a declarative base class, and creating a session maker.

"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Get the values from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_DATABASE_DEV')


# Create SQLAlchemy engine 
engine = create_engine("mysql+mysqlconnector://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name))
# Create Base class
Base = declarative_base()

# Create Session Maker 
Session = sessionmaker(bind=engine)
