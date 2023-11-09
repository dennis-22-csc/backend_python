"""

This module gets user and profile data from the database and prints them.

"""

from models import User, Profile
from config import Session

session = Session()
users = session.query(User).all()
profiles = session.query(Profile).all()

print("User data")
for user in users:
    print("id: {}, username: {}, profile_id: {}".format(user.id, user.username, user.profile_id))

print("")
print("Profile data")
for profile in profiles:
    print("id: {}, full name: {}".format(profile.id, profile.full_name))

# Close the session when done
session.close()
