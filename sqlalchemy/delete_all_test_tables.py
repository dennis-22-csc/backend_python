"""
This module deletes all test tables in a database using SQLAlchemy.

It includes a function for deleting tables in the database based on the SQLAlchemy Base model.

Functions:
	delete_all_tables(): Deletes all tables in the database. 
"""
from test_config import engine
from models import Base

def delete_all_tables():
	"""Deletes all tables in the database.
	
	Returns:
		String "Tables deleted successfully." if successful or an exception string if unsuccessful.
	"""
	try:
		Base.metadata.drop_all(engine)
		return "Tables deleted successfully."
	except Exception as e:
		return "Error occurred: {}".format(e)
		
if __name__ == "__main__":
	result = delete_all_tables()
	print(result)