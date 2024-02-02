import sys
import psycopg2

def list_users(host, port, password):
    cursor, conn = None, None
    try:
        # Establish a connection to the default 'postgres' database
        conn = psycopg2.connect(dbname='postgres', user='postgres', password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Retrieve the list of users
        cursor.execute("SELECT usename FROM pg_user;")
        users = cursor.fetchall()

        print("Existing PostgreSQL users:")
        for user in users:
            print(user[0])

    except psycopg2.Error as e:
        print(f"Error listing users: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Usage: python3 list_users.py <host> <port> <password>")
        sys.exit(1)

    # Extract command-line arguments
    host, port, password = sys.argv[1:]

    # Call the function to list users
    list_users(host, port, password)

#python3 list_users.py  localhost 5432 db_password

