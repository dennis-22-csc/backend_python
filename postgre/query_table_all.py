import sys
import psycopg2

def query_table_all(user, password, host, port, dbname):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()
        
        # Define the SQL statement to query the users table
        query_sql = f"SELECT * FROM users;"
        
        # Execute the SQL statement
        cursor.execute(query_sql)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            print(f"Users': {result}")
        else:
            print(f"No users in the 'users' table yet.")

    except psycopg2.Error as e:
        print(f"Error querying table: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 6:
        print("Usage: python3 query_table_all.py <user> <password> <host> <port> <dbname>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname = sys.argv[1:]

    # Call the function to query the specified database
    query_table_all(user, password, host, port, dbname)

# python3 query_table_all.py dennis db_password localhost 5432 collabio

