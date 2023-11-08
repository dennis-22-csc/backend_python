"""

This module defines SQLAlchemy models for User and Profile for a database.

It includes the User and Profile classes which are ORM models mapped to database tables.

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
    username = Column(String(255))
    profile_id = Column(Integer, ForeignKey('profiles.id'))
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
    full_name = Column(String(255))
    user = relationship('User', back_populates='profile')
