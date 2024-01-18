"""This module defines routes for interacting with the authentication server."""
from fastapi import APIRouter, HTTPException, Header, Depends, Query
from fastapi.responses import JSONResponse
from v1.oauth.views.utils import save_obj, validate_auth_code, has_expired, delete_obj, client_exist
from v1.oauth.views.auth_server import AuthServer
from models.auth_code import AuthCode
from models.access_token import AccessToken

router = APIRouter()

def get_auth_code_from_user(authorization: str = Header(None)):
    return {"auth_code": authorization}
    
def validate_grant_type(grant_type: str = Query(..., title="Grant Type", description="The type of grant")):
    if grant_type not in ["password", "client_credentials", "refresh_token"]:
        error_info = ["Bad Request", "Invalid grant_type specified."]
        raise HTTPException(status_code=400, detail=error_info)
    return grant_type
    
@router.post('/access_token')
def access_token(request_data: dict, grant_type: str = Depends(validate_grant_type)):
    client_id = request_data['client_id']
    client_secret = request_data['client_secret']
    
    auth_server = AuthServer()

    if not grant_type:
        error_info = ["Unauthorized", "Please provide a grant type."]
        raise HTTPException(status_code=401, detail=error_info)
        
    if grant_type != 'client_credentials':
        error_info = ["Unauthorized", grant_type]
        raise HTTPException(status_code=401, detail=error_info)
    if not client_id or not client_secret:
        error_info = ["Unauthorized", "Please provide a client id and client secret"]
        raise HTTPException(status_code=401, detail=error_info)

    if not auth_server.authenticate_client(client_id, client_secret):
        error_info = ["Unauthorized", "Please provide a valid client id and client secret"]
        raise HTTPException(status_code=401, detail=error_info)

    access_token_dict = auth_server.generate_access_token(client_id, client_secret)
    token_saved = save_obj(AccessToken, access_token_dict)
    if not token_saved:
        error_info = ["Internal Server Error", "An error occurred in the process of generating the token."]
        raise HTTPException(status_code=500, detail=error_info) 
    return JSONResponse(content=access_token_dict, status_code=201) 

@router.post('/auth_code')
def gen_auth_code(request_data: dict):
    if 'email' not in request_data:
        error_info = ["Bad Request", "The 'email' is required in the request body."]
        raise HTTPException(status_code=400, detail=error_info)

    if not request_data["email"]:
        error_info = ["Bad Request", "The 'email' must not contain an empty value."]
        raise HTTPException(status_code=400, detail=error_info)

    if not isinstance(request_data["email"], str):
        error_info = ["Bad Request", "The value of the 'email' field must be a string."]
        raise HTTPException(status_code=400, detail=error_info)

    if len(request_data.keys()) > 1:
        error_info = ["Bad Request", "You can't have more than the email field in the request json."]
        raise HTTPException(status_code=400, detail=error_info)

    auth_server = AuthServer()
    auth_code = auth_server.generate_auth_code(request_data["email"])
    saved_code = save_obj(AuthCode, auth_code)
    if not saved_code:
        error_info = ["Internal Server Error", "An error occurred in the process of generating auth code."]
        raise HTTPException(status_code=500, detail=error_info)

          
    return JSONResponse(content={"Success": auth_code}, status_code=201) 



@router.post('/register_client')
def register_client_endpoint(request_data: dict, code: dict = Depends(get_auth_code_from_user)):
    auth_code = code["auth_code"]
    
    if 'full_name' not in request_data or 'email' not in request_data or 'password' not in request_data:
        error_info = ["Bad Request", "The 'full_name', 'email', and 'password' fields are required in the request body."]
        raise HTTPException(status_code=400, detail=error_info)

    if not request_data["full_name"] or not request_data["email"] or not request_data["password"]:
        error_info = ["Bad Request", "The 'full_name', 'email', and 'password' fields must not contain empty values."]
        raise HTTPException(status_code=400, detail=error_info)

    if not isinstance(request_data["full_name"], str) or not isinstance(request_data["email"], str) or not isinstance(request_data["password"], str) :
        error_info = ["Bad Request", "The value of the 'full_name', 'email', and 'password' fields must be strings."]
        raise HTTPException(status_code=400, detail=error_info)

    if len(request_data.keys()) > 3:
        error_info = ["Bad Request", "You can't have more than three fields in the request json."]
        raise HTTPException(status_code=400, detail=error_info)

    if not auth_code:
        error_info = ["Unauthorized", "Please provide an authorization code."]
        raise HTTPException(status_code=401, detail=error_info)

    val_auth_code = validate_auth_code(auth_code, request_data["email"])
    if not val_auth_code:

        error_info = ["Unauthorized", "Please provide a valid authorization code."]
        raise HTTPException(status_code=401, detail=error_info)

    if has_expired(val_auth_code):
        delete_obj(val_auth_code)
        error_info = ["Unauthorized", "Authorization code has expired."]
        raise HTTPException(status_code=401, detail=error_info)

    
    auth_server = AuthServer()
    response = auth_server.register_client(request_data)
    return JSONResponse(content=response, status_code=201) 


@router.post('/client_secret')
def gen_new_secret(request_data: dict, code: dict = Depends(get_auth_code_from_user)):
    auth_code = code["auth_code"]
    
    if 'email' not in request_data:
        error_info = ["Bad Request", "The 'email' field is required in the request body."]
        raise HTTPException(status_code=400, detail=error_info)

    if not request_data["email"]:
        error_info = ["Bad Request", "The 'email' field must not contain an empty value."]
        raise HTTPException(status_code=400, detail=error_info)

    if not isinstance(request_data["email"], str):
        error_info = ["Bad Request", "The value of the 'email' field must be a string."]
        raise HTTPException(status_code=400, detail=error_info)

    if len(request_data.keys()) > 1:
        error_info = ["Bad Request", "You can't have more than one field in the request json."]
        raise HTTPException(status_code=400, detail=error_info)

    if not auth_code:
        error_info = ["Unauthorized", "Please provide an authorization code."]
        raise HTTPException(status_code=401, detail=error_info)

    val_auth_code = validate_auth_code(auth_code, request_data["email"])
    if not val_auth_code:
        error_info = ["Unauthorized", "Please provide a valid authorization code."]
        raise HTTPException(status_code=401, detail=error_info)

    if has_expired(val_auth_code):
        delete_obj(val_auth_code)
        error_info = ["Unauthorized", "Authorization code has expired."]
        raise HTTPException(status_code=401, detail=error_info)

    if not client_exist(request_data["email"]):
        error_info = ["Unauthorized", "You are not an existing client."]
        raise HTTPException(status_code=401, detail=error_info)

    auth_server = AuthServer()
    response = auth_server.generate_new_client_secret(request_data["email"])
    if not response:
        error_info = ["Internal Server Error", "An error occured when trying to update existing secret"]
        raise HTTPException(status_code=500, detail=error_info)

    return JSONResponse(content=response, status_code=201) 


@router.post('/client_password')
def gen_new_password(request_data: dict, code: dict = Depends(get_auth_code_from_user)):
    auth_code = code["auth_code"]
    
    if 'email' not in request_data or 'password' not in request_data:
        error_info = ["Bad Request", "The 'email' and 'password' fields are required in the request body."]

        raise HTTPException(status_code=400, detail=error_info)

    if not request_data["email"] or not request_data["password"]:
        error_info = ["Bad Request", "The 'email' and 'password' fields must not contain empty values."]

        raise HTTPException(status_code=400, detail=error_info)

    if not isinstance(request_data["email"], str) or not isinstance(request_data["password"], str):
        error_info = ["Bad Request", "The value of 'email' and 'password' fields must be strings."]

        raise HTTPException(status_code=400, detail=error_info)

    if len(request_data.keys()) > 2:
        error_info = ["Bad Request", "You can't have more than two fields in the request json."]

        raise HTTPException(status_code=400, detail=error_info)

   
    if not auth_code:
        error_info = ["Unauthorized", "Please provide an authorization code."]
        raise HTTPException(status_code=401, detail=error_info)


    val_auth_code = validate_auth_code(auth_code, request_data["email"])
    if not val_auth_code:

        error_info = ["Unauthorized", "Please provide a valid authorization code."]

        raise HTTPException(status_code=401, detail=error_info)
    if has_expired(val_auth_code):
        delete_obj(val_auth_code)
        error_info = ["Unauthorized", "Authorization code has expired."]
        raise HTTPException(status_code=401, detail=error_info)

    if not client_exist(request_data["email"]):
        error_info = ["Unauthorized", "You are not an existing client."]

        raise HTTPException(status_code=401, detail=error_info)
    auth_server = AuthServer()
    response = auth_server.generate_new_client_password(request_data["email"], request_data["password"])
    if not response:
        error_info = ["Internal Server Error", "An error occured when trying to update existing password"]
        raise HTTPException(status_code=500, detail=error_info)

    return JSONResponse(content=response, status_code=201) 

