import sys
import psycopg2

def delete_table_columns(user, password, host, port, dbname, *columns):
    cursor, conn = None, None  
    try:
        # Establish a connection to the specified database
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Execute a query that returns rows to get the column names
        cursor.execute("SELECT * FROM users LIMIT 0")
        
        # Extract column names from cursor.description
        column_names = [column[0] for column in cursor.description]

        # Create a temporary table with the desired structure (excluding columns to be deleted)
        # Drop the temporary table if it already exists
        temp_table_name = "users_temp"
        drop_temp_table_sql = f"DROP TABLE IF EXISTS {temp_table_name};"
        cursor.execute(drop_temp_table_sql)

        remaining_columns = [col for col in column_names if col not in columns]
        create_temp_table_sql = f"""
            CREATE TABLE {temp_table_name} AS
            SELECT {', '.join(remaining_columns)}
            FROM users;
        """
        cursor.execute(create_temp_table_sql)

        # Copy data from the existing table to the temporary table
        copy_data_sql = f"INSERT INTO {temp_table_name} ({', '.join(remaining_columns)}) SELECT {', '.join(remaining_columns)} FROM users;"
        cursor.execute(copy_data_sql)


        # Drop the existing table
        drop_table_sql = "DROP TABLE users;"
        cursor.execute(drop_table_sql)

        # Rename the temporary table to the original table name
        rename_table_sql = f"ALTER TABLE {temp_table_name} RENAME TO users;"
        cursor.execute(rename_table_sql)

        print(f"Columns {', '.join(columns)} deleted successfully from the 'users' table.")

    except psycopg2.Error as e:
        print(f"Error deleting table columns: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 7:
        print("Usage: python3 delete_table_columns.py <user> <password> <host> <port> <dbname> <column1> [<column2> ...]")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port, dbname = sys.argv[1:6]
    columns = sys.argv[6:]

    # Call the function to delete columns from the specified database table
    delete_table_columns(user, password, host, port, dbname, *columns)

# python3 delete_table_columns.py dennis db_password localhost 5432 collabio name

