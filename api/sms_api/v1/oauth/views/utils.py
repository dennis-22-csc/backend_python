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
    
def update_obj(class_name, info_dict, email):
    objs = storage.all(class_name)
    for obj in objs.values():
    	if email  == obj.email:
    		new_obj_dict = obj.to_dict()
    		for key in info_dict:
    			if key == "id":
    				continue
    			new_obj_dict[key] = info_dict[key]
    		new_obj = class_name(**new_obj_dict)
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

def email_client(client_address, subject, body):
    email_service = EmailService.create_email_service("gmail")
    email_service.send_email(client_address, subject, body) 
	
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
