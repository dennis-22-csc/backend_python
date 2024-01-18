import bcrypt
import secrets
import models
from datetime import datetime, timedelta
from models import storage
from models.base_model import BaseModel
from models.access_token import AccessToken
from models.api_client import Client
from models.auth_code import AuthCode

def has_expired(my_obj):
    """Checks if expirable objects has expired."""
    classes = [BaseModel, AccessToken, AuthCode]
    obj_dict = my_obj.to_dict()
    if type(my_obj) not in classes or "created_at" not in obj_dict or "expires_in" not in obj_dict:
    	raise ValueError("Didn't supply an expirable object")
    if models.storage_t == 'db':
        created_at = datetime.strptime(obj_dict["created_at"], '%Y-%m-%dT%H:%M:%S')
    else:
        created_at = datetime.strptime(obj_dict["created_at"], '%Y-%m-%dT%H:%M:%S.%f')
    expires_in_seconds = int(obj_dict["expires_in"])
    expiration_time = created_at + timedelta(seconds=expires_in_seconds)
    return datetime.now() > expiration_time

def delete_obj(my_obj):
    """
    Deletes an object.
    """
    classes = [BaseModel, AccessToken, AuthCode, Client]
    if type(my_obj) not in classes:
        raise ValueError("Didn't supply a valid object")
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
    classes = [BaseModel, AccessToken, AuthCode, Client]
    if class_name not in classes:
        raise ValueError("Didn't supply a valid object")
    new_obj = class_name(**obj_dict)
    new_obj.save()
    return new_obj
    
def update_obj(class_name, info_dict, email):
    """ Update object associated with email with information in dict"""
    classes = [Client]
    if class_name not in classes:
        raise ValueError("Didn't supply a valid object")
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

def get_client_ids():
    """ Get client ids from storage."""
    id_list = []
    auth_clients = storage.all(Client)
    for auth_client in auth_clients.values():
        id_list.append(auth_client.id)
    return id_list

def get_client_secrets():
    """ Get client secrets from storage."""
    secret_list = []
    auth_clients = storage.all(Client)
    for auth_client in auth_clients.values():
        secret_list.append(auth_client.secret)
    return secret_list
