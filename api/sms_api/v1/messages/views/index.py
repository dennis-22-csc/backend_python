"""This module defines routes for interacting with the SMS API."""

from v1.messages.views import app_views
from flask import jsonify, abort, request
from v1.messages.views.handlers import send_sms
from v1.oauth.views.utils import validate_token, has_expired, delete_token

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Get the status of the API.

    This endpoint returns a JSON response indicating the status of the API.

    Returns:
        A JSON response with the status information.
        Example:
        {
            "status": "OK"
        }
    """
    return jsonify({"status": "OK"})

@app_views.route('/sms', methods=['POST'])
def send_sms_endpoint():
    """
    Endpoint for sending SMS messages.

    Receives a JSON payload with 'to' and 'message' fields and sends an SMS.

    Returns:
        tuple: A tuple containing a JSON-formatted Response and the HTTP status code.

    Raises:
        400 Bad Request: If the required fields are missing or have empty values, among others.
        401 Unauthorized: If an access token is not provided, or is invalid, or has expired.

    """
    request_data = request.json
    access_token = request.headers.get("Authorization")
    
    if not access_token:
        error_info = ["Unauthorized", "Please provide an access token."]
        abort(401, error_info)
    val_access_token = validate_token(access_token)
    if not val_access_token:
        error_info = ["Unauthorized", "Please provide a valid access token."]
        abort(401, error_info)
    if has_expired(val_access_token):
        delete_token(val_access_token)
        error_info = ["Unauthorized", "Access token has expired."]
        abort(401, error_info)
    if 'to' not in request_data or 'message' not in request_data:
        error_info = ["Bad Request", "The 'to' and 'message' fields are required in the request body."]
        abort(400, error_info)
    if not request_data["to"] or not request_data["message"]:
        error_info = ["Bad Request", "The 'to' and 'message' fields must not contain empty values."]
        abort(400, error_info)
    if not isinstance(request_data["to"], list) or any(not value for value in request_data["to"]):
        error_info = ["Bad Request", "The value of the 'to' field must be a list containing at least one phone number."]
        abort(400, error_info)
    if any(not isinstance(element, str) for element in request_data["to"]):
        error_info = ["Bad Request", "The value of the 'to' field must be a list containing at least one string of phone numbers."]
        abort(400, error_info)
    if not isinstance(request_data["message"], str):
        error_info = ["Bad Request", "The value of the 'message' field must be a string."]
        abort(400, error_info)
    if len(request_data.keys()) > 2:
        error_info = ["Bad Request", "You can't have more than two fields in the request json."]
        abort(400, error_info)
    response = send_sms(request_data)
    return jsonify(response), 201

