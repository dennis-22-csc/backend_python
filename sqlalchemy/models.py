"""

This module defines SQLAlchemy models for a database.

It includes classes which are ORM models mapped to database tables.

"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class User(Base):
    """
    SQLAlchemy model representing user information in a 'users' table.

    Atrributes:
        id (int): Primary key for users table.
        username (str): User's username.
        profile_id (int): Foreign key referencing a profile's id.
        profile (Profile): One-to-one relationship with the Profile model

    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    profile = relationship('Profile', uselist=False, back_populates='user')

class Profile(Base):
    """
    SQLAlchemy model representing user profiles in the 'profiles' table.

    Attributes:
        id (int): Primary key for the 'profiles' table.
        full_name (str): User's full name.
        user (User): One-to-one relationship with the User model.

    """
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    user = relationship('User', back_populates='profile')

<<<<<<< HEAD
=======

>>>>>>> b4ac25981247b3d14c48334a354c0f6768e1565d
class Customer(Base):
    """
    SQLAlchemy model representing customer information in a 'customers' table.

    Atrributes:
        id (int): Primary key for users table.
        name (str): Customer's name.
        age (int): Customer's age.
    
    """
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
<<<<<<< HEAD
=======
    name = Column(String(25), nullable=False)
    age = Column(Integer, nullable=False)
>>>>>>> b4ac25981247b3d14c48334a354c0f6768e1565d
