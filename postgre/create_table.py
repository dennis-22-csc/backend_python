import sys
import psycopg2

def create_table(user, password, host, port, dbname):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()
        
        # Define the SQL statement to create the table (Modify for the specific table you want to create)
        table_name = "users"
        create_table_sql = f"CREATE TABLE {table_name} (user_id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, email VARCHAR(100) UNIQUE NOT NULL);"
        # Execute the SQL statement
        cursor.execute(create_table_sql)
        print(f"Table '{table_name}' created successfully in database '{dbname}'.")

    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 6:
        print("Usage: python3 create_table.py <user> <password> <host> <port> <dbname>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname = sys.argv[1:]

    # Call the function to create a table in the specified database
    create_table(user, password, host, port, dbname)

# python3 create_table.py dennis db_password localhost 5432 collabio

