from pydantic import BaseModel


###### Request #####

class PostCreateReq(BaseModel):
    title : str
    content : str
    img_id : str

class PostUpdateReq(BaseModel):
    post_id : str
    title : str
    content : str
    img_id : str

class PostDeleteReq(BaseModel):
    post_id:str

class PostDetailReq(BaseModel):
    post_id:str

class PostLikeReq(BaseModel):
    post_id:str

###### Response #####

class PostCreateRes(BaseModel):
    post_id:str

class PostList(BaseModel):
    post_id:str
    title: str
    user_id:str
    profile_id:str
    like_cnt:int
    comment_cnt:int
    view_cnt:int
    create_time:str

class PostListRes(BaseModel):
    posts:list[PostList]


class PostDetailRes(BaseModel):
    post_id:str
    title: str
    content: str
    user_id:str
    profile_id:str
    img_id:str
    like_cnt:int
    comment_cnt:int
    view_cnt:int
    create_time:str
    like_YN:str
