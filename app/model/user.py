from pydantic import BaseModel

class User(BaseModel):
    user_id : str
    password : str
    nickname : str
    img_id : str