import sys
import psycopg2

def query_table_user(user, password, host, port, dbname, username):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()
        
        # Define the SQL statement to query the users table for information about a specific user
        query_sql = f"SELECT * FROM users WHERE username = '{username}';"
        
        # Execute the SQL statement
        cursor.execute(query_sql)

        # Fetch the result
        result = cursor.fetchone()

        if result:
            print(f"User information for '{username}': {result}")
        else:
            print(f"No user found with the username '{username}' in the 'users' table.")

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
    if len(sys.argv) != 7:
        print("Usage: python3 query_table_user.py <user> <password> <host> <port> <dbname> <username>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname, username = sys.argv[1:]

    # Call the function to query the specified database
    query_table_user(user, password, host, port, dbname, username)

# python3 query_table_user.py dennis db_password localhost 5432 collabio dennis

