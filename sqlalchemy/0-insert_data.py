"""

This module creates a new user and a corresponding profile in the database.

"""

from models import User, Profile
from config import Session

# Create a new user and a corresponding profile
new_user = User(username='dennis', profile=Profile(full_name='Akpotaire Dennis'))
session = Session()
session.add(new_user)
session.commit()
session.close()
