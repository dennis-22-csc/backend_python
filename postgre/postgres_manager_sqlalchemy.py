from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

class SQLAlchemyPostgresManager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def connect(self):
        try:
            self.session = self.Session()
            return True
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return False

    def create_table(self, table_class):
        try:
            table_class.metadata.create_all(self.engine)
            print(f"Table '{table_class.__tablename__}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def insert_table(self, table_class, **kwargs):
        try:
            new_record = table_class(**kwargs)
            self.session.add(new_record)
            self.session.commit()
            print(f"Record inserted successfully into the '{table_class.__tablename__}' table.")
        except Exception as e:
            print(f"Error inserting record: {e}")

    def query_table_all(self, table_class):
        try:
            records = self.session.query(table_class).all()
            if records:
                for record in records:
                    print(f"Record: {record.__dict__}")
            else:
                print(f"No records in the '{table_class.__tablename__}' table yet.")
        except Exception as e:
            print(f"Error querying table: {e}")

    def query_table_user(self, table_class, username):
        try:
            record = self.session.query(table_class).filter_by(username=username).first()
            if record:
                print(f"User information for '{username}': {record.__dict__}")
            else:
                print(f"No user found with the username '{username}' in the '{table_class.__tablename__}' table.")
        except Exception as e:
            print(f"Error querying table: {e}")

    def update_table_row(self, table_class, username, new_values):
        try:
            record = self.session.query(table_class).filter_by(username=username).first()
            if record:
                for key, value in new_values.items():
                    setattr(record, key, value)
                self.session.commit()
                print(f"Row updated successfully for user '{username}' in the '{table_class.__tablename__}' table.")
            else:
                print(f"No user found with the username '{username}' in the '{table_class.__tablename__}' table. No updates performed.")
        except Exception as e:
            print(f"Error updating table row: {e}")

    def delete_table_row(self, table_class, username):
        try:
            record = self.session.query(table_class).filter_by(username=username).first()
            if record:
                self.session.delete(record)
                self.session.commit()
                print(f"User '{username}' deleted successfully from the '{table_class.__tablename__}' table.")
            else:
                print(f"No user found with the username '{username}' in the '{table_class.__tablename__}' table. No deletions performed.")
        except Exception as e:
            print(f"Error deleting table row: {e}")

    def add_table_columns(self, table_class, *columns):
        try:
            for column in columns:
                setattr(table_class, column, Column(String(50)))
            table_class.metadata.create_all(self.engine)
            print(f"Columns {', '.join(columns)} added successfully to the '{table_class.__tablename__}' table.")
        except Exception as e:
            print(f"Error adding table columns: {e}")

    def delete_table(self, table_class):
        try:
            table_class.__table__.drop(self.engine)
            print(f"Table '{table_class.__tablename__}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting table: {e}")

    def close_connection(self):
        if self.session:
            self.session.close()
            print("Connection closed.")

if __name__ == "__main__":
    db_url = "postgresql://dennis:db_password@localhost/collabio"
    db = SQLAlchemyPostgresManager(db_url)
    db.connect()
    db.create_table(User)
    db.insert_table(User, username='dennis', email='denniskoko@gmail.com')
    db.query_table_all(User)
    db.query_table_user(User, 'dennis')
    db.update_table_row(User, 'dennis', {'email': 'denniskoko@yahoo.com'})
    db.query_table_user(User, 'dennis')
    db.delete_table_row(User, 'dennis')
    db.query_table_user(User, 'dennis')
    db.add_table_columns(User, 'first_name', 'last_name', 'age')
    db.close_connection()
    db.delete_table(User)
    

