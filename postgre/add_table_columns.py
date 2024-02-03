import sys
import psycopg2

def add_table_columns(user, password, host, port, dbname, *columns):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Loop through the provided column names and add them to the table
        for column in columns:
            # Define the SQL statement to add a column to the users table
            add_column_sql = f"ALTER TABLE users ADD COLUMN {column} VARCHAR(50);"
            
            # Execute the SQL statement
            cursor.execute(add_column_sql)
            print(f"Column '{column}' added successfully to the 'users' table.")

    except psycopg2.Error as e:
        print(f"Error adding table columns: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 7:
        print("Usage: python3 add_table_columns.py <user> <password> <host> <port> <dbname> <column1> [<column2> ...]")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname = sys.argv[1:6]
    columns = sys.argv[6:]

    # Call the function to add columns to the specified database table
    add_table_columns(user, password, host, port, dbname, *columns)

# python3 add_table_columns.py dennis db_password localhost 5432 collabio name age

