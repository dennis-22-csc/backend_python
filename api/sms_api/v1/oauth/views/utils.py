import bcrypt
import secrets
from datetime import datetime, timedelta
from models import storage
from models.access_token import AccessToken
from models.api_client import Client
from models.auth_code import AuthCode
from v1.oauth.views.email_service import EmailService

def has_expired(token_obj):
    """Checks if token object has expired."""
    token_dict = token_obj.to_dict()
    created_at = datetime.strptime(token_dict["created_at"], '%Y-%m-%dT%H:%M:%S.%f')
    expires_in_seconds = int(token_dict["expires_in"])
    expiration_time = created_at + timedelta(seconds=expires_in_seconds)
    return datetime.now() > expiration_time

def delete_token(token_obj):
    """
    Deletes a token object.
    """
    storage.delete(token_obj)
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

def save_token(token_dict):
    """Creates new access token."""
    new_token = AccessToken(**token_dict)
    new_token.save()
    return True

def hash_password(password):
    """Hashes a password using a random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password, password):
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

def save_client(client_dict):
    """Creates and persists a client to storage ."""
    new_client = Client(**client_dict)
    new_client.save()
    return new_client

def email_client(client_email, subject, body, app):
    email_service = EmailService.create_email_service("gmail", app)
    email_service.send_email(client_email, subject, body) 
	
def generate_auth_code():
    """
    Generates a six-digit authorization code.

    Returns:
    - str: The generated auth code.
    """
    auth_code = str(secrets.randbelow(1000000)).zfill(6)
    return auth_code

def save_auth_code(code):
    """Creates and persists an authorization code to storage ."""
    new_code = AuthCode(**{"code": code})
    new_code.save()
    return True
