"""This module defines an authentication server that can be used to authenticate the clients of an API and generate access tokens."""

import json
import hmac
import hashlib
import time
import base64
import secrets
from v1.oauth.views.utils import hash_password, generate_client_secret, save_client, generate_auth_code, save_auth_code, email_client

class AuthServer():
    """Defines an authentication server."""
    def __init__(self):
        """Creates instance of an authentication server."""
        self.client_ids = ["1", "2", "3"]
        self.client_secrets = ["4", "5", "6"]
        
	def send_auth_code(self, client_email):
		auth_code = generate_auth_code()
		saved_code = save_auth_code(auth_code)
		if not saved_code:
			error_info = ["Internal Server Error", "An error occurred in the process of generating auth code."]
			abort(500, error_info)
		email_subject = "Authorization Code"
		email_body = f"Hi there,\n\n"
        email_body += f"You recently requested for an authorization code for the DennisCode SMS API!\n"
        email_body += f"Below is the code:\n\n"
        email_body += auth_code + "\n\n"
        email_body += f"Best regards,\n"
        email_body += f"DennisCode"
		email_client(client_email, email_subject, email_body)
		
    def register_client(self, client_payload):
        client_payload["password"] = hash_password(client_payload["password"])
        client_payload["secret"] = generate_client_secret()
        saved_client = save_client(client_payload)
        if not saved_client:
        	error_info = ["Internal Server Error", "An error occurred in the process of registering your info."]
			abort(500, error_info)
		return {"status": "success", "client_id": saved_client.id, "client_secret", saved_client.secret}

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
        return {'access_token': access_token, 'expires_in': 10000}