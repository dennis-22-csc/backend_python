"""

This module queries the customers table returning and printing the id, name, age and a dynamically generated age_group data.

The age_group data is dynamically generated for each customer using the case function.

"""

from models import Customer
from config import Session
from sqlalchemy import case

session = Session()

# Query the 'customers' table
customers = session.query(Customer.id, Customer.name, Customer.age, case(
        {
            Customer.age < 21: 'Under 21',
            Customer.age < 30: '21-29',
            Customer.age < 40: '30-39',
            Customer.age < 50: '40-49',
            Customer.age < 60: '50-59',
            Customer.age >= 60: '60 and Over',
        }
    ).label('age_group'))

print("Customer data")
for customer in customers:
    print("id: {}, name: {}, age: {}, age_group: {}".format(customer.id, customer.name, customer.age, customer.age_group))