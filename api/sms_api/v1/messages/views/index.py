"""This module defines routes for interacting with the SMS API."""

from v1.messages.views import app_views
from flask import jsonify


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
