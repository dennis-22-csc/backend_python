"""This module defines routes for interacting with the SMS API."""

from v1.messages.views import app_views
from flask import jsonify, abort, request
from v1.messages.views.handlers import send_sms 

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

    Args:
        None

    Returns:
        tuple: A tuple containing a JSON-formatted Response and the HTTP status code.

    Raises:
        400 Bad Request: If the required fields are missing or have empty values,
                        or if 'to' is not a list or contains invalid elements.

    Example:
        Example usage when making a POST request to send an SMS:
        >>> import requests
        >>> data = {"to": ["1234567890"], "message": "Hello, world!"}
        >>> response = requests.post("http://example.com/sms", json=data)
        >>> print(response.status_code, response.json())
    """
    request_data = request.json

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

