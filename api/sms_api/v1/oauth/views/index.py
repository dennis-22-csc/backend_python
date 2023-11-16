"""This module defines routes for interacting with the authentication server."""

from v1.oauth.views import app_views
from flask import jsonify, abort, request, current_app
from v1.oauth.views.utils import save_obj, validate_auth_code, has_expired, delete_obj
from v1.oauth.views.auth_server import AuthServer

@app_views.route('/access_token', methods=['POST'], strict_slashes=False)
def access_token():
    """

    Endpoint for generating an access token.

    Recieves a json payload with client_id and client_secret fields together with a grant_type query parameter.

    Returns:
        tuple: A tuple containing a json formatted dictionary and an HTTP status code. In the dictionary is the access token and the expiration time.

    Raises:
        401 Unauthorized: If the required fields and query parameters are missing, or not valid.
        500 Internal Server Error: If the token was not successfully persisted.
        
    """
    grant_type = request.args.get('grant_type')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    
    auth_server = AuthServer()

    if not grant_type:
        error_info = ["Unauthorized", "Please provide a grant type."]
        abort(401, error_info)
        
    if grant_type != 'client_credentials':
        error_info = ["Unauthorized", grant_type]
        abort(401, error_info)
    if not client_id or client_secret:
        error_info = ["Unauthorized", "Please provide a client id and client secret"]
        abort(401, error_info)

    if not auth_server.authenticate_client(client_id, client_secret):
        error_info = ["Unauthorized", "Please provide a valid client id and client secret"]
        abort(401, error_info)

    access_token_dict = auth_server.generate_access_token(client_id, client_secret)
    token_saved = save_obj(access_token_dict)
    if not token_saved:
        error_info = ["Internal Server Error", "An error occurred in the process of generating the token."]
        abort(500, error_info)
    return jsonify(access_token_dict), 201  

@app_views.route('/auth_code', methods=['POST'])
def gen_auth_code():
    """
    Endpoint for generating authentication code.

    Receives a JSON payload with 'email' field, generates an auth code and send code to email.

    Returns:
        tuple: A tuple containing a JSON-formatted Response and the HTTP status code.

    Raises:
        400 Bad Request: If the email field is missing or has empty value, among others.

    """
    request_data = request.json 
    if 'email' not in request_data:
        error_info = ["Bad Request", "The 'email' is required in the request body."]
        abort(400, error_info)
    if not request_data["email"]:
        error_info = ["Bad Request", "The 'email' must not contain an empty value."]
        abort(400, error_info)
    if not isinstance(request_data["email"], str):
        error_info = ["Bad Request", "The value of the 'email' field must be a string."]
        abort(400, error_info)
    if len(request_data.keys()) > 1:
        error_info = ["Bad Request", "You can't have more than the email field in the request json."]
        abort(400, error_info)
    auth_server = AuthServer()
    auth_server.send_auth_code(request_data["email"])
    return jsonify({"Success": "Authorization code sent to email"}), 201


@app_views.route('/register_client', methods=['POST'])
def register_client_endpoint():
    """
    Endpoint for registering clients.

    Receives a JSON payload with 'full_name', 'email', and 'password' fields and registers the client.

    Returns:
        tuple: A tuple containing a JSON-formatted Response and the HTTP status code.

    Raises:
        400 Bad Request: If the required fields are missing or have empty values, among others.
        401 Unauthorized: If an authorization code is not provided, or is invalid, or has expired.

    """
    request_data = request.json
    auth_code = request.headers.get("Authorization")
    
    if 'full_name' not in request_data or 'email' not in request_data or 'password' not in request_data:
        error_info = ["Bad Request", "The 'full_name', 'email', and 'password' fields are required in the request body."]
        abort(400, error_info)
    if not request_data["full_name"] or not request_data["email"] or not request_data["password"]:
        error_info = ["Bad Request", "The 'full_name', 'email', and 'password' fields must not contain empty values."]
        abort(400, error_info)
    #if not isinstance(request_data["full_name"], str) or isinstance(request_data["email"], str) or isinstance(request_data["password"], str) :
        #error_info = ["Bad Request", "The value of the 'full_name', 'email', and 'password' fields must be strings."]
        #abort(400, error_info)
    if len(request_data.keys()) > 3:
        error_info = ["Bad Request", "You can't have more than three fields in the request json."]
        abort(400, error_info)
    if not auth_code:
        error_info = ["Unauthorized", "Please provide an authorization code."]
        abort(401, error_info)
    val_auth_code = validate_auth_code(auth_code, request_data["email"])
    if not val_auth_code:

        error_info = ["Unauthorized", "Please provide a valid authorization code."]
        abort(401, error_info)
    if has_expired(val_auth_code):
        delete_obj(val_auth_code)
        error_info = ["Unauthorized", "Authorization code has expired."]
        abort(401, error_info)
    
    auth_server = AuthServer()
    response = auth_server.register_client(request_data)
    return jsonify(response), 201

