"""

This module creates a new user in a database.
It contains a function that creates a new user in a database. 

Functions:
    create_user(session, user): Add a new user to the database.

"""

from models import User, Profile

def create_user(session, user):
    """Create a new user in the database.
    Args:
        session (Session): The Session object for database interaction.
        user (User): The new user to be added to the database.
    
    Returns:
        An integer representing success or failure. 1 for success. -1 for failure.

    Usage:
    result = create_user(session, user)

    """
    try:
        session.add(user)
        session.commit()
        return 1
    except Exception:
        return -1

if __name__ == "__main__":
    new_user = User(username='dennis', profile=Profile(full_name='Akpotaire Dennis'))
    Session = __import__("config").Session
    with Session() as db_session:
        result = create_user(db_session, new_user)
        print("result: ", result)
