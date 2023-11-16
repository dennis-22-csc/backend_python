from models.base_model import BaseModel
class AccessToken(BaseModel):
    """
    Represents an access token.

    This class defines attributes such as access_token, expires_in.
    It inherits the attributes and methods of a class BaseModel.

    Attributes:
        access_token (str): the access token. 
        expires_in (str): time in seconds the access token expires. 
    """
    access_token = ""
    expires_in = ""
