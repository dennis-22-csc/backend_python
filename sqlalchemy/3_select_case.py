"""

This module queries the customers table returning and printing the id, name, age and a dynamically generated age_group data.

The age_group data is dynamically generated for each customer using the case function.

Functions:
	get_customers_dynamically_generating_age_group_data_for_each_customer(session): Gets customers dynamically generating age group data for each customer. 
	
"""

from models import Customer
from sqlalchemy import case

def get_customers_dynamically_generating_age_group_data_for_each_customer(session):
    """Gets customers dynamically generating age group data for each customer.
	
	Args:
		session (Session): Database session to be used for database operations.
	
	Returns:
        A list or an exception string. 
        If a list, list is either empty or has vustomer objects having an age_group attribute. 
	
	Usage:
		result = get_customers_dynamically_generating_age_group_data_for_each_customer(session)
	"""
    try:
        return session.query(Customer.id, Customer.name, Customer.age, case(
        {
            Customer.age < 21: 'Under 21',
            Customer.age < 30: '21-29',
            Customer.age < 40: '30-39',
            Customer.age < 50: '40-49',
            Customer.age < 60: '50-59',
            Customer.age >= 60: '60 and Over',
        }
    ).label('age_group')).all()

    except Exception as e:
       return f"Error occurred: {e}"


if __name__ == "__main__":
    Session = __import__("config").Session
    with Session() as db_session:
        result = get_customers_dynamically_generating_age_group_data_for_each_customer(db_session)
        if isinstance(result, list):
            print("Customer data")
            if result:
                for customer in result:
                    print("id: {}, name: {}, age: {}, age_group: {}".format(customer.id, customer.name, customer.age, customer.age_group))
            else:
                print("No data yet")
        else:
           print(result)
