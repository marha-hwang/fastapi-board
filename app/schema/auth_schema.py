from pydantic import BaseModel


class Login(BaseModel):
    user_id:str
    password:str

class UserInfo(BaseModel):
    user_id:str
    nickname:str
    img_id:str

class LoginResponse(BaseModel):
    access_token : str
    token_type : str
    user : UserInfo