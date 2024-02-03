import sys
import psycopg2

def update_table_row(user, password, host, port, dbname, username, new_email):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()
        
        # Define the SQL statement to update the email of a specific user in the users table
        update_sql = f"UPDATE users SET email = '{new_email}' WHERE username = '{username}';"
        
        # Execute the SQL statement
        cursor.execute(update_sql)

        # Check if any row was affected
        if cursor.rowcount > 0:
            print(f"Email updated successfully for user '{username}' in the 'users' table.")
        else:
            print(f"No user found with the username '{username}' in the 'users' table. No updates performed.")

    except psycopg2.Error as e:
        print(f"Error updating table row: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 8:
        print("Usage: python3 update_table_row.py <user> <password> <host> <port> <dbname> <username> <new_email>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname, username, new_email = sys.argv[1:]

    # Call the function to update a row in the specified database
    update_table_row(user, password, host, port, dbname, username, new_email)

# python3 update_table_row.py dennis db_password localhost 5432 collabio dennis denniskoko@yahoo.com

