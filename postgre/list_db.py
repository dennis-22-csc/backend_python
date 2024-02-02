import sys
import psycopg2

def list_user_databases(user, password, host, port):
    cursor, conn = None, None
    try:
        # Establish a connection to the 'postgres' database
        conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
        conn.autocommit = True  # Set autocommit to True

        cursor = conn.cursor()

        # Retrieve the OID of the specified user
        cursor.execute("SELECT usesysid FROM pg_user WHERE usename = %s;", (user,))
        user_oid = cursor.fetchone()[0]

        # Retrieve the list of databases associated with the specified user
        cursor.execute("SELECT datname FROM pg_database WHERE datdba = %s;", (user_oid,))
        databases = cursor.fetchall()

        print("Databases associated with user '{}':".format(user))
        for db in databases:
            print(db[0])

    except psycopg2.Error as e:
        print(f"Error listing databases: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 5:
        print("Usage: python3 list_db.py <user> <password> <host> <port>")
        sys.exit(1)

    # Extract command-line arguments
    user, password, host, port = sys.argv[1:]

    # Call the function to list databases associated with the specified user
    list_user_databases(user, password, host, port)

#python3 list_db.py postgres db_password localhost 5432

