from pydantic import BaseModel

class Request(BaseModel):
    user_id:str


class Response(BaseModel):
    success:bool
    message:str