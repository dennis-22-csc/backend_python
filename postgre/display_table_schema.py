import sys
import psycopg2

def display_table_schema(user, password, host, port, dbname, table_name):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Execute a query to get the table schema
        cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}';")
        
        # Fetch all rows from the result
        rows = cursor.fetchall()

        # Display the table schema
        if rows:
            print(f"Schema for table '{table_name}':")
            for row in rows:
                print(f"{row[0]}: {row[1]}")
        else:
            print(f"Table '{table_name}' not found in the database.")

    except psycopg2.Error as e:
        print(f"Error displaying table schema: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 7:
        print("Usage: python3 display_table_schema.py <user> <password> <host> <port> <dbname> <table_name>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname, table_name = sys.argv[1:]

    # Call the function to display the schema of the specified table
    display_table_schema(user, password, host, port, dbname, table_name)

