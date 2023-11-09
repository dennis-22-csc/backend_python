"""
This module initializes and creates database tables using SQLAlchemy for testing purposes.

It includes a function for creating tables in the database based on the SQLAlchemy Base model.

Functions:
	create_tables(): Creates tables in the database. 
"""
from test_config import engine
from models import Base

def create_tables():
	"""Create tables in the database.
	
	Returns:
		String "Tables created successfully." if successful or an exception string if unsuccessful.
	"""
	try:
		Base.metadata.create_all(engine)
		return "Tables created successfully."
	except Exception as e:
		return "Error occurred: {}".format(e)
		
if __name__ == "__main__":
	result = create_tables()
	print(result)
	