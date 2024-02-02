import sys
import psycopg2
from psycopg2 import sql

def create_user(new_user, password, host, port):
    cursor, conn = None, None
    try:
        # Establish a connection to the default 'postgres' database
        conn = psycopg2.connect(dbname='postgres', user='postgres', password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Use psycopg2.sql.SQL to safely insert the new user and password into the SQL query
        create_user_query = sql.SQL("CREATE USER {} WITH ENCRYPTED PASSWORD %s;").format(sql.Identifier(new_user))

        # Execute the query to create the new user
        cursor.execute(create_user_query, (password,))

        print(f"User '{new_user}' created successfully.")

    except psycopg2.Error as e:
        print(f"Error creating user: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 5:
        print("Usage: python3 create_user.py <new_user> <password> <host> <port>")
        sys.exit(1)

    # Extract command-line arguments
    new_user, password, host, port = sys.argv[1:]

    # Call the function to create the new user
    create_user(new_user, password, host, port)

#python3 create_user.py dennis db_password localhost 5432

