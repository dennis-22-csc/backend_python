"""

This module gets user and profile data from the database.
It includes functions that gets user and profile data from the database using SQLAlchemy. 

Functions:
	get_users(session): Gets users from the database. 
	get_profiles(session): Get persisted profiles from the database. 
	
"""

from models import User, Profile

def get_users(session):
    """Gets users.

    Args:
        session (Session): Database session.
    Returns:
        A list of user objects or an empty list if successful or an exception string if unsuccessful.
    Usage:
        result = get_users(session)
    """

    try:
        return session.query(User).all()
    except Exception as e:
        return f"Error occurred: {e}"

def get_profiles(session):
    """Gets profile from the database.

    Args:
        session (Session): Database session.
    Returns:
        A list of profile objects or an empty list if successful or an exception string if unsuccessful.
    Usage:
        result = get_profiles(session)
    """
    try:
        return session.query(Profile).all()
    except Exception as e:
        return f"Error occurred: {e}"

if __name__ == "__main__":
    Session = __import__("config").Session
    with Session() as db_session:
        result = get_users(db_session)

        if isinstance(result, list):
            if result:
                print("User data")
                for user in result:
                    print(f"id: {user.id}, username: {user.username}, profile_id: {user.profile_id}")
            else:
                print("No user saved yet")
        else:
            print(result)

        result = get_profiles(db_session)
        print("")
        if isinstance(result, list):
            if result:
                print("Profile data")
                for profile in result:
                    print(f"id: {profile.id}, full name: {profile.full_name}")
            else:
                print("No user profile saved yet")
        else:
            print(result)
