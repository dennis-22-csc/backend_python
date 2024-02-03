import psycopg2

class PostgresManager:
    def __init__(self, dbname='postgres', user='postgres', password=None, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.conn.autocommit = True
            return True
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return False

    def create_table(self, table_name, columns):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Define the SQL statement to create the table
            create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns)});"
            
            # Execute the SQL statement
            cursor.execute(create_table_sql)

            print(f"Table '{table_name}' created successfully in database '{self.dbname}'.")
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
        finally:
            if cursor:
                cursor.close()

    def insert_table(self, table_name, columns, values):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Define the SQL statement to insert a new record into the table
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {tuple(values)};"

            # Execute the SQL statement
            cursor.execute(insert_sql)

            print(f"Record inserted successfully into the '{table_name}' table in database '{self.dbname}'.")
        except psycopg2.Error as e:
            print(f"Error inserting record: {e}")
        finally:
            if cursor:
                cursor.close()

    def query_table_all(self, table_name):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Define the SQL statement to query the table
            query_sql = f"SELECT * FROM {table_name};"
            
            # Execute the SQL statement
            cursor.execute(query_sql)

            # Fetch all results
            results = cursor.fetchall()

            if results:
                for result in results:
                    print(f"Record: {result}")
            else:
                print(f"No records in the '{table_name}' table yet.")
        except psycopg2.Error as e:
            print(f"Error querying table: {e}")
        finally:
            if cursor:
                cursor.close()

    def query_table_user(self, table_name, username):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Define the SQL statement to query the table for a specific user
            query_sql = f"SELECT * FROM {table_name} WHERE username = '{username}';"
            
            # Execute the SQL statement
            cursor.execute(query_sql)

            # Fetch the result
            result = cursor.fetchone()

            if result:
                print(f"User information for '{username}': {result}")
            else:
                print(f"No user found with the username '{username}' in the '{table_name}' table.")
        except psycopg2.Error as e:
            print(f"Error querying table: {e}")
        finally:
            if cursor:
                cursor.close()

    def update_table_row(self, table_name, username, new_values):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Create the SET part of the UPDATE statement with variadic columns
            set_columns = ', '.join(f"{col} = %s" for col in new_values.keys())

            # Define the SQL statement to update the values of a specific user in the table
            update_sql = f"UPDATE {table_name} SET {set_columns} WHERE username = '{username}';"
            
            # Execute the SQL statement
            cursor.execute(update_sql, tuple(new_values.values()))

            # Check if any row was affected
            if cursor.rowcount > 0:
                print(f"Row updated successfully for user '{username}' in the '{table_name}' table.")
            else:
                print(f"No user found with the username '{username}' in the '{table_name}' table. No updates performed.")
        except psycopg2.Error as e:
            print(f"Error updating table row: {e}")
        finally:
            if cursor:
                cursor.close()



    def delete_table_row(self, table_name, username):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Define the SQL statement to delete a specific user from the table
            delete_sql = f"DELETE FROM {table_name} WHERE username = '{username}';"
            
            # Execute the SQL statement
            cursor.execute(delete_sql)

            # Check if any row was affected
            if cursor.rowcount > 0:
                print(f"User '{username}' deleted successfully from the '{table_name}' table.")
            else:
                print(f"No user found with the username '{username}' in the '{table_name}' table. No deletions performed.")
        except psycopg2.Error as e:
            print(f"Error deleting table row: {e}")
        finally:
            if cursor:
                cursor.close()

    def add_table_columns(self, table_name, *columns):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Loop through the provided column names and add them to the table
            for column in columns:
                # Define the SQL statement to add a column to the table
                add_column_sql = f"ALTER TABLE {table_name} ADD COLUMN {column} VARCHAR(50);"
                
                # Execute the SQL statement
                cursor.execute(add_column_sql)
                print(f"Column '{column}' added successfully to the '{table_name}' table.")
        except psycopg2.Error as e:
            print(f"Error adding table columns: {e}")
        finally:
            # Close the cursor
            if cursor:
                cursor.close()

    def delete_table_columns(self, table_name, *columns):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Execute a query that returns rows to get the column names
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")

            # Extract column names from cursor.description
            column_names = [column[0] for column in cursor.description]

            # Create a temporary table with the desired structure (excluding columns to be deleted)
            # Drop the temporary table if it already exists
            temp_table_name = f"{table_name}_temp"
            drop_temp_table_sql = f"DROP TABLE IF EXISTS {temp_table_name};"
            cursor.execute(drop_temp_table_sql)

            remaining_columns = [col for col in column_names if col not in columns]
            create_temp_table_sql = f"""
                CREATE TABLE {temp_table_name} AS
                SELECT {', '.join(remaining_columns)}
                FROM {table_name};
            """
            cursor.execute(create_temp_table_sql)

            # Copy data from the existing table to the temporary table
            copy_data_sql = f"INSERT INTO {temp_table_name} ({', '.join(remaining_columns)}) SELECT {', '.join(remaining_columns)} FROM {table_name};"
            cursor.execute(copy_data_sql)

            # Drop the existing table
            drop_table_sql = f"DROP TABLE {table_name};"
            cursor.execute(drop_table_sql)

            # Rename the temporary table to the original table name
            rename_table_sql = f"ALTER TABLE {temp_table_name} RENAME TO {table_name};"
            cursor.execute(rename_table_sql)

            print(f"Columns {', '.join(columns)} deleted successfully from the '{table_name}' table.")
        except psycopg2.Error as e:
            print(f"Error deleting table columns: {e}")
        finally:
            # Close the cursor
            if cursor:
                cursor.close()

    def delete_table(self, table_name):
        cursor = None
        try:
            if not self.conn:
                if not self.connect():
                    return

            cursor = self.conn.cursor()

            # Define the SQL statement to delete the table
            delete_table_sql = f"DROP TABLE IF EXISTS {table_name};"
            
            # Execute the SQL statement
            cursor.execute(delete_table_sql)
            print(f"Table '{table_name}' deleted successfully from database '{self.dbname}'.")

        except psycopg2.Error as e:
            print(f"Error deleting table: {e}")

        finally:
            # Close the cursor
            if cursor:
                cursor.close()

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")
            
if __name__ == "__main__":
    db = PostgresManager(dbname='collabio', user='dennis', password='db_password')
    db.create_table('users', ['user_id SERIAL PRIMARY KEY', 'username VARCHAR(50) UNIQUE NOT NULL', 'email VARCHAR(100) UNIQUE NOT NULL'])
    db.insert_table('users', ['username', 'email'], ('dennis', 'denniskoko@gmail.com'))
    db.query_table_all('users')
    db.query_table_user('users', 'dennis')
    db.update_table_row('users', 'dennis', {'email': 'denniskoko@yahoo.com'})
    db.query_table_user('users', 'dennis')
    db.delete_table_row('users', 'dennis')
    db.query_table_user('users', 'dennis')
    db.delete_table('users')
    db.close_connection()
