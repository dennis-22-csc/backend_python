import sys
import psycopg2
from psycopg2 import sql

def delete_database(dbname, user, password, host, port):
    try:
        # Establish a connection to the default 'postgres' database
        conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Use psycopg2.sql.SQL to safely insert the database name into the SQL query
        drop_database_query = sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(dbname))

        # Execute the query to drop the specified database
        cursor.execute(drop_database_query)

        print(f"Database '{dbname}' deleted successfully.")

    except psycopg2.Error as e:
        print(f"Error deleting database: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 6:
        print("Usage: python3 delete_db.py <database_name> <user> <password> <host> <port>")
        sys.exit(1)

    # Extract command-line arguments
    dbname, user, password, host, port = sys.argv[1:]

    # Call the function to delete the database
    delete_database(dbname, user, password, host, port)

#python3 delete_db.py hello_db postgres db_password localhost 5432

