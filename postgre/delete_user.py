import sys
import psycopg2
from psycopg2 import sql

def delete_user(user_to_delete, host, port, password):
    cursor, conn = None, None
    try:
        # Establish a connection to the default 'postgres' database
        conn = psycopg2.connect(dbname='postgres', user='postgres', password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Use psycopg2.sql.SQL to safely insert the user name into the SQL query
        delete_user_query = sql.SQL("DROP USER IF EXISTS {};").format(sql.Identifier(user_to_delete))

        # Execute the query to delete the specified user
        cursor.execute(delete_user_query)

        print(f"User '{user_to_delete}' deleted successfully.")

    except psycopg2.Error as e:
        print(f"Error deleting user: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 5:
        print("Usage: python3 delete_user.py <user_to_delete> <host> <port> <password>")
        sys.exit(1)

    # Extract command-line arguments
    user_to_delete, host, port, password = sys.argv[1:]

    # Call the function to delete the user
    delete_user(user_to_delete, host, port, password)

#python3 delete_user.py dennis  localhost 5432 db_password

