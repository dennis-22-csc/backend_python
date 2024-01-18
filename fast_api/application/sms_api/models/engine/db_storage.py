import models
from models.base_model import BaseModel, Base
from models.access_token import AccessToken
from models.api_client import Client
from models.auth_code import AuthCode
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


#Load environment variables from .env file
load_dotenv()

classes = {"AccessToken": AccessToken, "Client": Client, "AuthCode": AuthCode} 

class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        SMS_API_MYSQL_USER = os.getenv('SMS_API_MYSQL_USER')
        SMS_API_MYSQL_PWD = os.getenv('SMS_API_MYSQL_PWD')
        SMS_API_MYSQL_HOST = os.getenv('SMS_API_MYSQL_HOST')
        SMS_API_MYSQL_DB = os.getenv('SMS_API_MYSQL_DB')
        SMS_API_ENV = os.getenv('SMS_API_ENV')
        self.__engine = create_engine('mysql+mysqlconnector://{}:{}@{}/{}'.
                                      format(SMS_API_MYSQL_USER,
                                             SMS_API_MYSQL_PWD,
                                             SMS_API_MYSQL_HOST,
                                             SMS_API_MYSQL_DB))
        if SMS_API_ENV == "test":
            Base.metadata.drop_all(self.__engine)
            
    @property
    def engine(self):
        return self.__engine        

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
