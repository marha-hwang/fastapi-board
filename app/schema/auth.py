from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id:str
    password:str

class User(BaseModel):
    user_id:str
    nickname:str
    img_id:str

class LoginResponse(BaseModel):
    access_token : str
    token_type : str
    user : User