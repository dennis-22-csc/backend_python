import bcrypt
import secrets
from datetime import datetime, timedelta
from models import storage
from models.access_token import AccessToken
from models.api_client import Client
from models.auth_code import AuthCode
from v1.oauth.views.email_service import EmailService

def has_expired(my_obj):
    """Checks if expirable objects has expired."""
    obj_dict = my_obj.to_dict()
    created_at = datetime.strptime(obj_dict["created_at"], '%Y-%m-%dT%H:%M:%S.%f')
    expires_in_seconds = int(obj_dict["expires_in"])
    expiration_time = created_at + timedelta(seconds=expires_in_seconds)
    return datetime.now() > expiration_time

def delete_obj(my_obj):
    """
    Deletes an object.
    """
    storage.delete(my_obj)
    storage.save()
    return True

def validate_token(token_value):
    """
    Checks if token exists.
    """

    access_tokens = storage.all(AccessToken)
    for access_token in access_tokens.values():
        if token_value == access_token.access_token:
            return access_token
    return None

def save_obj(class_name, obj_dict):
    """Creates new object in storage."""
    new_obj = class_name(**obj_dict)
    new_obj.save()
    return new_obj

def hash_password(password):
    """Hashes a password using a random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid_password(hashed_password, password):
    """Checks if the hashed password was formed from the given password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
   
def generate_client_secret(length=32):
    """
    Generate a random client secret.

    Args:
    - length (int): The length of the client secret.

    Returns:
    - str: The generated client secret.
    """
    client_secret = secrets.token_urlsafe(length)
    return client_secret


def email_client(client_address, subject, body):
    email_service = EmailService.create_email_service("gmail")
    email_service.send_email(client_address, subject, body) 
	
def generate_auth_code(client_email):
    """
    Generates a six-digit authorization code.

    Returns:
    - str: The generated auth code.
    """
    auth_code = str(secrets.randbelow(1000000)).zfill(6)
    return {"code": auth_code, "client_email": client_email, "expires_in": 900}

def validate_auth_code(code, email):
    """
    Checks if auth code exists for client.
    """

    auth_codes = storage.all(AuthCode)
    for auth_code in auth_codes.values():
        if code == auth_code.code and email == auth_code.client_email:
            return auth_code
    return None
    
def client_exist(email):
    """
    Checks if new client exists.
    """

    auth_clients = storage.all(Client)
    for auth_client in auth_clients.values():
        if email == auth_client.email:
            return True
    return False
