from models.base_model import BaseModel
class AuthCode(BaseModel):
	code = ""
	client_email = ""
	expires_in = ""
