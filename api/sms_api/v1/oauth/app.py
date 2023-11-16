import json
from flask import Flask, Response
from v1.oauth.views import app_views
from os import environ
from v1.oauth.config import GMAIL_SMTP_SETTINGS


app = Flask(__name__)
app.register_blueprint(app_views)
app.json.sort_keys = False
app.config["GMAIL_SMTP_SETTINGS"] = GMAIL_SMTP_SETTINGS

def handle_error(error):
    """
    Handle errors as defined using app.errorhandler and formats them into a JSON response.

    Args:
        error (Exception): The error object containing information about the error.

    Returns:
        tuple: A tuple containing a JSON-formatted Response and the HTTP status code.
    """
    error_response = {"code": error.code}

    if isinstance(error.description, list):
        error_response["reason"] = error.description[0]
        error_response["message"] = error.description[1]
    elif isinstance(error.description, str):
        error_response["reason"] = error.name
        error_response["message"] = error.description

    error_json = json.dumps(error_response, indent=1)
    formatted_error_data = error_json[0] + '\n' + error_json[1:-1].replace('  , ', ',\n') + '\n' + error_json[-1]

    return Response(formatted_error_data, content_type='application/json'), error.code

app.errorhandler(400)(handle_error)
app.errorhandler(500)(handle_error)
app.errorhandler(404)(handle_error)
app.errorhandler(401)(handle_error)


if __name__ == "__main__":
    """
    This script runs a Flask application for the authentication component of an SMS API.

    It sets up the host and port, and runs the application.

    Environment Variables:
        - SMS_API_HOST: Host IP address to run the API (default: '0.0.0.0')
        - SMS_API_PORT: Port number for the API (default: '5000')

    Example:
        $ export SMS_API_HOST='127.0.0.1'
        $ export SMS_API_PORT='8080'
        $ python3 app.py
    """
    host = environ.get('SMS_API_HOST', '0.0.0.0')
    port = environ.get('SMS_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
