from typing import Any
from fastapi import APIRouter
from app.core.security import get_current_user
import app.schema.common_schema as common_schema
import app.schema.post_schema as post_schema
import app.service.post_service as post_service
import app.config as config
from app.repository.base_post_repository import BasePostRepository
from app.repository.db.db_post_repository import PostRepositoryDB
from app.repository.csv.csv_post_repository import PostRepositoryCSV
from app.repository.base_like_repository import BaseLikePostRepository
from app.repository.db.db_like_repository import LikeRepositoryDB
from app.repository.csv.csv_like_repository import LikePostRepositoryCSV
from app.repository.base_user_repository import BaseUserRepository
from app.repository.db.db_user_repository import UserRepositoryDB
from app.repository.csv.csv_user_repository import UserRepositoryCSV
from app.repository.base_comment_repository import BaseCommentRepository
from app.repository.db.db_comment_repository import CommentRepositoryDB
from app.repository.csv.csv_comment_repository import CommentRepositoryCSV


from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session

def get_post_repository(db:Session = Depends(get_db)):
    if config.db_type == "database" :
        return PostRepositoryDB(db)
    else:
        return PostRepositoryCSV()

def get_like_repository(db:Session = Depends(get_db)):
    if config.db_type == "database" :
        return LikeRepositoryDB(db)
    else:
        return LikePostRepositoryCSV()
    
def get_comment_repository(db:Session = Depends(get_db)):
    if config.db_type == "database" :
        return CommentRepositoryDB(db)
    else:
        return CommentRepositoryCSV()
def get_user_repository(db:Session = Depends(get_db)):
    if config.db_type == "database" :
        return UserRepositoryDB(db)
    else:
        return UserRepositoryCSV()


router = APIRouter(tags=["게시글"], prefix="/post")

@router.post("", response_model=common_schema.ApiResponse)
async def create_post(request: post_schema.PostCreateReq, current_user: str = Depends(get_current_user), repo:BasePostRepository = Depends(get_post_repository)) -> Any:

    result = post_service.create_post(repo, request, current_user)
    response = common_schema.ApiResponse(success=True,
                                        message="게시글 작성에 성공하였습니다.",
                                        data=post_schema.PostCreateRes(post_id=result)) 
    return response

@router.delete("", response_model=common_schema.ApiResponse)
async def remove_post(request: post_schema.PostDeleteReq, current_user: str = Depends(get_current_user), repo:BasePostRepository = Depends(get_post_repository)) -> Any:

    post_service.remove_post(repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="게시글 삭제에 성공하였습니다.") 

    return response

@router.put("", response_model=common_schema.ApiResponse)
async def update_post(request: post_schema.PostUpdateReq, current_user: str = Depends(get_current_user), repo:BasePostRepository = Depends(get_post_repository)) -> Any:

    post_service.update_post(repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="게시글 업데이트에 성공하였습니다.") 

    return response

@router.post("/like", response_model=common_schema.ApiResponse)
async def update_post_like(request: post_schema.PostLikeReq,
                            current_user: str = Depends(get_current_user),
                            like_repo:BaseLikePostRepository = Depends(get_like_repository)) -> Any:

    post_service.update_post_like(like_repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="좋아요 업데이트에 성공하였습니다.") 

    return response

@router.get("", response_model=common_schema.ApiResponse)
async def view_list_post(current_user: str = Depends(get_current_user),
                            post_repo:BasePostRepository = Depends(get_post_repository),
                            like_repo:BaseLikePostRepository = Depends(get_like_repository),
                            user_repo:BaseUserRepository = Depends(get_user_repository),
                            comment_repo:BaseCommentRepository = Depends(get_comment_repository)) -> Any:

    result = post_service.get_post_list(post_repo, like_repo, user_repo, comment_repo)
    response = common_schema.ApiResponse[post_schema.PostListRes](success=True, message="게시글 조회에 성공하였습니다.", data=result) 
    return response

@router.get("/{post_id}", response_model=common_schema.ApiResponse)
async def view_detail_post(post_id:str, current_user: str = Depends(get_current_user),
                           post_repo:BasePostRepository = Depends(get_post_repository),
                           like_repo:BaseLikePostRepository = Depends(get_like_repository),
                           user_repo:BaseUserRepository = Depends(get_user_repository),
                           comment_repo:BaseCommentRepository = Depends(get_comment_repository)) -> Any:

    result = post_service.get_post_detail(post_repo, like_repo, user_repo, comment_repo, post_id, current_user)
    response = common_schema.ApiResponse[post_schema.PostDetailRes](success=True, message="게시글 조회에 성공하였습니다.", data=result) 
    return response
