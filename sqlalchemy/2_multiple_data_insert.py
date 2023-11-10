"""

This module creates multiple customers in the database.

Functions:
	insert_customers_from_dict_list(session, customers_list): Creates customers in the database from a list of dictionary of customer info. 
	
"""

from models import Customer

def insert_customers_from_dict_list(session, customers_list):
    """Receives a list of dictionaries storing customer information and creates corresponding customers in the database.

    Args:
	    session (Session): Database session object to be used for the insert operation. 
	    customers_list (list(dict)): List of dictionaries storing customer information. 
	    Returns:
	        String Customers added successfully if successful or an exception string if not successful. 
	    Usage:
		    result = insert_customers_from_dict_list(db_session, customers)
    """
    try:
        for customer_dict in customers_list:
            customer = Customer(name=customer_dict['name'], age=customer_dict['age'])
            session.add(customer)
        session.commit()
        return "Customers added successfully"
    except Exception as e:
        return f"Error occured: {e}"

if __name__ == "__main__":
    Session = __import__("config").Session
    load = __import__("json").load

    try:
        with Session() as db_session, open("customers.json", "r", encoding="utf-8") as f:
            customers = load(f)
            result = insert_customers_from_dict_list(db_session, customers)
            print(result)
    except Exception as e:
        print(e)
