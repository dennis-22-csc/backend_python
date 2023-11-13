from flask import Flask
from v1.messages.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)

if __name__ == "__main__":
    """
    This script runs a Flask application for an SMS API.

    It registers blueprints, sets up the host and port, and runs the application.

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