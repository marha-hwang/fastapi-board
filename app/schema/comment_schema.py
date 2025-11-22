from pydantic import BaseModel


###### Request #####

class CommentCreateReq(BaseModel):
    post_id : str
    comment : str

class CommentUpdateReq(BaseModel):
    comment_id : str
    comment : str

class CommentDeleteReq(BaseModel):
    comment_id:str


###### Response #####

class Comment(BaseModel):
    comment_id:str
    content: str
    user_id:str
    profile_id:str|None = None
    create_time:str

class CommentListRes(BaseModel):
    comments:list[Comment]
