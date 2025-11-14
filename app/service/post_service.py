import app.schema.post_schema as post_schema
import app.model.models as app_models
import app.core.security as security
import app.crud.post_crud as post_crud
import app.crud.like_crud as like_crud
import app.core.util as util
import logging

logger = logging.getLogger(__name__)

def create_post(input: post_schema.PostCreateReq, user_id:str)->str :

    # Post model객체 생성하여 crud 수행
    new_post_id = util.generate_random_string()
    post = app_models.Post(
        post_id=new_post_id,
        user_id=user_id,
        title=input.title,
        content=input.content,
        img_id=input.img_id,
        view_cnt=0,
        create_time=util.get_current_time_string()
    )

    if post_crud.insert_post(post=post) : return new_post_id
    else : return None

def remove_post(input:post_schema.PostDeleteReq, user_id:str)->str :

    post = post_crud.select_post(post_id=input.post_id)
    if post == None : return "해당 게시글이 존재하지 않습니다."
    if post.user_id != user_id : return "자신이 작성한 글만 삭제 가능합니다."

    if post_crud.delete_post(post_id=input.post_id) : return "게시글 삭제가 성공적으로 완료되었습니다."
    else : return "게시글 삭제에 실패하였습니다." 


def update_post(input:post_schema.PostUpdateReq, user_id:str)->str :
    
    post = post_crud.select_post(post_id=input.post_id)
    if post == None : return "해당 게시글이 존재하지 않습니다."
    if post.user_id != user_id : return "자신이 작성한 게시글만 수정 가능합니다."

    # Post model객체 생성하여 crud 수행
    post = app_models.Post(
        post_id=input.post_id,
        user_id=user_id,
        title=input.title,
        content=input.content,
        img_id=input.img_id,
        view_cnt=post.view_cnt,
        create_time=post.create_time
    )

    if post_crud.update_post(post=post) : return "게시글 업데이트가 성공적으로 완료되었습니다."
    else : return "게시글 업데이트에 실패하였습니다."


def get_post_list()->post_schema.PostListRes :

    post_list = post_crud.select_post_all()
    if post_list == None : return None
    return post_list

def get_post_detail(post_id:str, user_id:str)->post_schema.PostDetailRes :

    post_detail = post_crud.select_post_detail(post_id=post_id, user_id=user_id)
    post_crud.increase_view_post_cnt(post_id=post_id)
    if post_detail == None : return None
    return post_detail

def update_post_like(input:post_schema.PostLikeReq, user_id:str)->str :

    # if post_crud.select_post(post_id=input.post_id) == None : return "해당 게시글이 존재하지 않습니다."

    # post_id, user_id를 통해 좋아요 여부 존재 확인 
    like_exist = like_crud.select_like(post_id=input.post_id, user_id=user_id)

    # 좋아요 없으면 추가
    if like_exist == None :
        like_crud.insert_like(post_id=input.post_id, user_id=user_id)
        return "좋아요를 추가하였습니다."
    # 좋아요 있으면 제거
    else : 
        like_crud.delete_like(post_id=input.post_id, user_id=user_id)
        return "좋아요를 제거하였습니다."
