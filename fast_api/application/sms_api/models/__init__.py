import os
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

storage_t = os.getenv("SMS_API_TYPE_STORAGE")
storage = None
if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
storage.reload()
