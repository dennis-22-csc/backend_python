# API

## Description
This directory contains every projects I create to learn more about building APIs.
The directory will be updated as I tackle more API projects that expand my knowledge of APIs.

## Content

#### `sms_api/v1` directory containing modules for an SMS API.

- [app.py](sms_api/v1/messages/app.py) - Python script that runs a Flask application for the SMS API.
- [init.py](sms_api/v1/messages/views/__init__.py) - Python script that defines a Flask Blueprint for the SMS API.
- [index.py](sms_api/v1/messages/views/index.py) - Python module that defines routes for interacting with the SMS API.
- [handlers.py](sms_api/v1/messages/views/handlers.py) - Python module that defines helper functions for the flask routes in the SMS API.

#### `sms_api/tests` directory contains all unit test cases for the SMS API modules.

- [test_api_status.py](sms_api/tests/test_api_status.py) - Python module that tests the end point for getting the status of the sms api.
- [test_send_sms.py](sms_api/tests/test_send_sms.py) - Python module that tests the end point for sms using the sms api.

