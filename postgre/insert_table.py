import sys
import psycopg2

def insert_table(user, password, host, port, dbname):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()
        
        # Define the SQL statement to insert a new record into the users table (Modify for the specific data you want to insert)
        username ="dennis"
        email ="denniskoko@gmail.com"
        insert_sql = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}');"
        
        # Execute the SQL statement
        cursor.execute(insert_sql)
        print(f"Record inserted successfully into the 'users' table in database '{dbname}'.")

    except psycopg2.Error as e:
        print(f"Error inserting record: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 6:
        print("Usage: python3 insert_table.py <user> <password> <host> <port> <dbname>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname = sys.argv[1:]

    # Call the function to insert a record into the specified database
    insert_table(user, password, host, port, dbname)

# python3 insert_table.py dennis db_password localhost 5432 collabio

