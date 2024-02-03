import sys
import psycopg2

def delete_table_row(user, password, host, port, dbname, username):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()
        
        # Define the SQL statement to delete a specific user from the users table
        delete_sql = f"DELETE FROM users WHERE username = '{username}';"
        
        # Execute the SQL statement
        cursor.execute(delete_sql)

        # Check if any row was affected
        if cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully from the 'users' table.")
        else:
            print(f"No user found with the username '{username}' in the 'users' table. No deletions performed.")

    except psycopg2.Error as e:
        print(f"Error deleting table row: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 7:
        print("Usage: python3 delete_table_row.py <user> <password> <host> <port> <dbname> <username>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname, username = sys.argv[1:]

    # Call the function to delete a row from the specified database
    delete_table_row(user, password, host, port, dbname, username)

# python3 delete_table_row.py dennis db_password localhost 5432 collabio dennis

