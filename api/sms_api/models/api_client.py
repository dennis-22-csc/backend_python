from models.base_model import BaseModel
class Client(BaseModel):
    """
    Represents an API client.

    This class defines such attributes as 'secret', 'full_name', 'email', and 'password'. 
    It inherits the attributes and methods of a class BaseModel.

    Attributes:
        secret (str): a password-like string that will be used to authenticate the client. 
        full_name (str): full name of the client. 
        password (str): password of the client. 
        email (str): email of the client. 
        
    """
    full_name = ""
    password = ""
    email = ""
    secret = "" 
