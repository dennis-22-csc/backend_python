"""This module defines routes for interacting with the SMS API."""

from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from v1.messages.views.handlers import send_sms
from v1.oauth.views.utils import validate_token, has_expired, delete_obj

router = APIRouter()

def get_access_token_from_user(authorization: str = Header(None)):
    return {"access_token": authorization}
    
@router.get('/status', response_model=dict)
async def status():
    return {"status": "OK"}

@router.post('/sms', response_model=dict)
async def send_sms_endpoint(request_data: dict, token: dict = Depends(get_access_token_from_user)):
    access_token = token["access_token"]
    
    if not access_token:
        error_info = ["Unauthorized", "Please provide an access token."]
        raise HTTPException(status_code=401, detail=error_info)
    val_access_token = validate_token(access_token)
    if not val_access_token:
        error_info = ["Unauthorized", "Please provide a valid access token."]
        raise HTTPException(status_code=401, detail=error_info)
    if has_expired(val_access_token):
        delete_obj(val_access_token)
        error_info = ["Unauthorized", "Access token has expired."]
        raise HTTPException(status_code=401, detail=error_info)
    if 'to' not in request_data or 'message' not in request_data:
        error_info = ["Bad Request", "The 'to' and 'message' fields are required in the request body."]
        raise HTTPException(status_code=400, detail=error_info)
    if not request_data["to"] or not request_data["message"]:
        error_info = ["Bad Request", "The 'to' and 'message' fields must not contain empty values."]
        raise HTTPException(status_code=400, detail=error_info)
    if not isinstance(request_data["to"], list) or any(not value for value in request_data["to"]):
        error_info = ["Bad Request", "The value of the 'to' field must be a list containing at least one phone number."]
        raise HTTPException(status_code=400, detail=error_info)
    if any(not isinstance(element, str) for element in request_data["to"]):
        error_info = ["Bad Request", "The value of the 'to' field must be a list containing at least one string of phone numbers."]
        raise HTTPException(status_code=400, detail=error_info)
    if not isinstance(request_data["message"], str):
        error_info = ["Bad Request", "The value of the 'message' field must be a string."]
        raise HTTPException(status_code=400, detail=error_info)
    if len(request_data.keys()) > 2:
        error_info = ["Bad Request", "You can't have more than two fields in the request json."]
        raise HTTPException(status_code=400, detail=error_info)
    response = send_sms(request_data)
    return JSONResponse(content=response, status_code=201)
