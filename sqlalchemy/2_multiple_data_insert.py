"""

This module creates multiple customers in the database.

Functions:
	insert_customers_from_dict_list(session, customers_list): Creates customers in the database from a list of dictionary of customer info. 
	
"""

from models import Customer
import logging

logging.basicConfig(filename='database.log', level=logging.INFO)

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
    failure_count = 0
    try:
        if not isinstance(customers_list, list):
            raise ValueError("Injected customer data not in a list.")
        for customer_dict in customers_list:
            if not isinstance(customer_dict, dict):
                failure_count += 1
                logging.info(f"{customer_dict} is not a dictionary.")
                continue
            try:
                customer = Customer(name=customer_dict['name'], age=customer_dict['age'])
                session.add(customer)
            except KeyError:
                failure_count += 1
                logging.info(f"{customer_dict} doesn't have a correct key.")
                continue
        session.commit()
        if failure_count == 0:
            return "Customers added successfully"
        else:
            return f"Added all customers except {failure_count}. Check the database log for more details."
    except Exception as e:
        return f"Error occurred: {e}"

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
