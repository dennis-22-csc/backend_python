"""This module defines an authentication server that can be used to authenticate the clients of an API and generate access tokens."""

import json
import hmac
import hashlib
import time
import base64
import secrets
from v1.oauth.views.utils import hash_password, save_obj, email_client, client_exist, update_obj, get_client_ids, get_client_secrets
from flask import abort
from models.api_client import Client
from models.auth_code import AuthCode

class AuthServer():
    """Defines an authentication server."""
    def __init__(self):
        """Creates instance of an authentication server."""
        self.client_ids = get_client_ids()
        self.client_secrets = get_client_secrets()
    def send_auth_code(self, client_email):
        email_subject = "Authorization Code"
        email_body = f"Hi there,\n\n"
        email_body += f"You recently requested for an authorization code for the DennisCode SMS API.\n"
        email_body += f"Below is the code:\n\n"
        email_body += auth_code["code"] + "\n\n"
        email_body += f"Please note that this code will expire in fifteen minutes time.\n"
        email_body += f"Best regards,\n"
        email_body += f"DennisCode"
        email_client(client_email, email_subject, email_body)

    def register_client(self, client_payload):
        if client_exist(client_payload["email"]):
            error_info = ["Internal Server Error", "Email address already exists."]
            abort(500, error_info)
        client_payload["password"] = hash_password(client_payload["password"]).decode("utf-8")
        client_payload["secret"] = self.generate_client_secret()
        saved_client = save_obj(Client, client_payload)
        if not saved_client:
            error_info = ["Internal Server Error", "An error occurred in the process of registering your info."]
            abort(500, error_info)
        return {"status": "success", "client_id": saved_client.id, "client_secret": saved_client.secret}

    def authenticate_client(self, client_id, client_secret):
        """Authenticates clients of an API.
        Args:
            client_id (str): id of the client.
            client_secret (str): password-like string acting as client secret.
        Returns:
            False if the client is not a registered client. True otherwise.
        """
        if client_id not in self.client_ids or client_secret not in self.client_secrets:
            return False
        return True

    def generate_access_token(self, client_id, client_secret):
        """Uses a combination of timestamp, random part, and client_id to create a unique token.
        Args:
            client_id (str): id of the client.
            client_secret (str): password-like string acting as client secret.
        Returns:
            dictionary containing generated access token and the time it expires.
        """
        timestamp = str(int(time.time()))
        # Generate a random part using the secrets module
        random_part = secrets.token_hex(16)  # 16 bytes (32 characters) in hexadecimal
        # Construct the message to be signed
        message = f"{timestamp}:{random_part}:{client_id}"
        # Convert the client_secret to bytes
        secret_bytes = bytes(client_secret, 'utf-8')
        # Use HMAC-SHA256 to sign the message
        signature = hmac.new(secret_bytes, message.encode('utf-8'), hashlib.sha256).digest()
        # Encode the signature in base64
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        # Construct the access token by combining the timestamp, random part, and signature
        access_token = f"{timestamp}.{random_part}.{signature_base64}"
        return {'access_token': access_token, 'expires_in': 900}
    def generate_auth_code(self, client_email):
        """
        Generates a six-digit authorization code.

        Returns:
            str: The generated auth code.
        """
        auth_code = str(secrets.randbelow(1000000)).zfill(6)
        return {"code": auth_code, "client_email": client_email, "expires_in": 200900}
   
    def generate_client_secret(self, length=32):
        """
        Generate a random client secret.

        Args:
            length (int): The length of the client secret.

        Returns:
            str: The generated client secret.
        """
        client_secret = secrets.token_urlsafe(length)
        return client_secret

    def generate_new_client_secret(self, email):
        new_secret = self.generate_client_secret()
        new_obj = update_obj(Client, {"secret": new_secret}, email)
        return {"client_id": new_obj.id, "new_client_secret": new_obj.secret}
        
    def generate_new_client_password(self, email, new_password):
        hashed_password = hash_password(new_password).decode("utf-8")
        new_obj = update_obj(Client, {"password": hashed_password}, email)
        return {"client_id": new_obj.id, "new_client_password": new_obj.password}
