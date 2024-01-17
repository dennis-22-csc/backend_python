from config import engine
from models import Base

def create_tables():
    try:
        Base.metadata.create_all(engine)
        return "Tables created successfully."
    except Exception as e:
        return "Error occurred: {}".format(e)

if __name__ == "__main__":
    result = create_tables()
    print(result)
