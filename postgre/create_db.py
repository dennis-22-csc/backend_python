import sys
import psycopg2
from psycopg2 import sql

def create_database(dbname, user, password, host, port):
    cursor, conn = None, None
    try:
        # Establish a connection to the PostgreSQL server
        conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
        conn.autocommit = True # Set autocommit to True
        
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Use psycopg2.sql.SQL to safely insert the database name into the SQL query
        create_database_query = sql.SQL("CREATE DATABASE {};").format(sql.Identifier(dbname))

        # Execute the query to create the new database
        cursor.execute(create_database_query)

        # Commit the changes
        conn.commit()


        print(f"Database '{dbname}' created successfully.")

    except psycopg2.Error as e:
        print(f"Error creating database: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 6:
        print("Usage: python3 create_db.py <new_database_name> <user> <password> <host> <port>")
        sys.exit(1)

    # Extract command-line arguments
    new_database_name, user, password, host, port = sys.argv[1:]

    create_database(new_database_name, user, password, host, port)

#python3 create_db.py hello_db postgres db_password localhost 5432

