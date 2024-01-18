from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from v1.oauth.views.index import router as oauth_router
from os import environ
import uvicorn

app = FastAPI()
app.include_router(oauth_router, prefix="/v1/oauth")

if __name__ == "__main__":
    """
    This script runs a FASTAPI application for the authentication component of an SMS API.

    It sets up the host and port, and runs the application.

    Environment Variables:
        - SMS_API_HOST: Host IP address to run the API (default: '0.0.0.0')
        - SMS_API_PORT: Port number for the API (default: '8000')

    Example:
        $ export SMS_API_HOST='127.0.0.1'
        $ export SMS_API_PORT='8080'
        $ python3 app.py
    """
    host = environ.get('SMS_API_HOST', '0.0.0.0')
    port = environ.get('SMS_API_PORT', '8000')
    uvicorn.run(app, host=host, port=port, reload=True)

