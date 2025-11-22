import app.schema.post_schema as post_schema
import app.model.models as app_models
import app.core.security as security
from app.repository.base_post_repository import BasePostRepository
from app.repository.base_like_repository import BaseLikePostRepository
from app.repository.base_user_repository import BaseUserRepository
from app.repository.base_comment_repository import BaseCommentRepository
import logging
from app.core.exception import CustomException, ErrorCode
import app.core.util as util

logger = logging.getLogger(__name__)

def create_post(repo:BasePostRepository, data: post_schema.PostCreateReq, user_id:str)->str :
    
    new_post_id = util.generate_random_string()
    post = app_models.Post(
        post_id=new_post_id,
        user_id=user_id,
        title=data.title,
        content=data.content,
        img_id=data.img_id,
        view_cnt=0,
        create_time=util.get_current_time_string()
    )
    try :
        repo.insert_post(post)
        return new_post_id
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="게시글 작성에 실패하였습니다.")


def remove_post(repo:BasePostRepository, data:post_schema.PostDeleteReq, user_id:str) :

    post = repo.select_post(data.post_id)
    if post == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="존재하지 않는 게시글입니다.")
    
    if post.user_id != user_id : 
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="자신이 작성한 글만 삭제 가능합니다.")

    try :
        repo.delete_post(data.post_id)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="게시글 삭제에 실패하였습니다.")

def update_post(repo:BasePostRepository, data:post_schema.PostUpdateReq, user_id:str) :
    
    post = repo.select_post(data.post_id)
    if post == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="존재하지 않는 게시글입니다.")
    
    if post.user_id != user_id : 
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="자신이 작성한 글만 삭제 가능합니다.")

    post = app_models.Post(
                post_id=data.post_id,
                user_id=user_id,
                title=data.title,
                content=data.content,
                img_id=data.img_id,
                view_cnt=post.view_cnt,
                create_time=post.create_time
            )

    try :
        repo.update_post(post)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="게시글 업데이트에 실패하였습니다.")

def update_post_like(like_repo:BaseLikePostRepository,
                     data:post_schema.PostLikeReq,
                     user_id:str) :

    # post_id, user_id를 통해 좋아요 여부 존재 확인 
    like_exist = like_repo.select_like(data.post_id, user_id)

    try :
        # 좋아요 없으면 추가
        if like_exist == None :
            like_repo.insert_like(post_id=data.post_id, user_id=user_id)
        # 좋아요 있으면 제거
        else : 
            like_repo.delete_like(post_id=data.post_id, user_id=user_id)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="좋아요 업데이트에 실패 하였습니다.")

def get_post_list(post_repo:BasePostRepository,
                    like_repo:BaseLikePostRepository,
                    user_repo:BaseUserRepository,
                    comment_repo:BaseCommentRepository)->post_schema.PostDetailRes :

    post_all = post_repo.select_post_all()
    post_list = []

    for post in post_all:
        user = user_repo.select_user(post.user_id)
        profile_id = user.img_id if user != None else None
        like_cnt = like_repo.select_like_cnt(post.post_id)
        comment_cnt = comment_repo.select_comment_cnt(post.post_id)
        like_yn = "Y" if like_repo.select_like(post.post_id, post.user_id) != None else "N"

        p = post_schema.PostList(
            post_id=post.post_id,
            title=post.title,
            content=post.content,
            user_id=post.user_id,
            profile_id=profile_id,
            img_id=post.img_id,
            like_cnt=like_cnt,
            comment_cnt=comment_cnt,
            view_cnt=post.view_cnt,
            create_time=str(post.create_time),
            like_YN=like_yn
        )
        post_list.append(p)
    result = post_schema.PostListRes(posts=post_list)
    return result

def get_post_detail(post_repo:BasePostRepository,
                    like_repo:BaseLikePostRepository,
                    user_repo:BaseUserRepository,
                    comment_repo:BaseCommentRepository,
                    post_id:str,
                    user_id:str)->post_schema.PostDetailRes :

    post_detail = post_repo.select_post(post_id)
    if post_detail == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="존재하지 않는 게시글입니다.")
    
    # 조회수 증가
    post_repo.increase_view_post_cnt(post_id)

    user = user_repo.select_user(user_id)
    profile_id = user.img_id if user != None else None
    like_cnt = like_repo.select_like_cnt(post_detail.post_id)
    comment_cnt = comment_repo.select_comment_cnt(post_detail.post_id)
    like_yn = "Y" if like_repo.select_like(post_detail.post_id, user_id) != None else "N"

    result = post_schema.PostDetailRes(
        post_id=post_detail.post_id,
        title=post_detail.title,
        content=post_detail.content,
        user_id=post_detail.user_id,
        profile_id=profile_id,
        img_id=post_detail.img_id,
        like_cnt=like_cnt,
        comment_cnt=comment_cnt,
        view_cnt=post_detail.view_cnt,
        create_time=str(post_detail.create_time),
        like_YN=like_yn
    )

    return result
