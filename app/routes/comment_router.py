from typing import Any
from fastapi import APIRouter
from app.core.security import get_current_user
import app.schema.common_schema as common_schema
import app.schema.comment_schema as comment_schema
import app.service.comment_service as comment_service
from app.repository.base_comment_repository import BaseCommentRepository
from app.repository.db.db_comment_repository import CommentRepositoryDB
from app.repository.csv.csv_comment_repository import CommentRepositoryCSV
from app.repository.base_user_repository import BaseUserRepository
from app.repository.db.db_user_repository import UserRepositoryDB
from app.repository.csv.csv_user_repository import UserRepositoryCSV
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
import app.config as config

router = APIRouter(tags=["댓글"], prefix="/comment")

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

@router.post("", response_model=common_schema.ApiResponse)
async def create_comment(request: comment_schema.CommentCreateReq, current_user: str = Depends(get_current_user), repo:BaseCommentRepository = Depends(get_comment_repository)) -> Any:

    comment_service.create_comment(repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="댓글 작성에 성공하였습니다.") 

    return response

@router.delete("", response_model=common_schema.ApiResponse)
async def remove_comment(request: comment_schema.CommentDeleteReq, current_user: str = Depends(get_current_user), repo:BaseCommentRepository = Depends(get_comment_repository)) -> Any:

    comment_service.remove_comment(repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="댓글 삭제에 성공하였습니다.") 

    return response

@router.put("", response_model=common_schema.ApiResponse)
async def update_comment(request: comment_schema.CommentUpdateReq, current_user: str = Depends(get_current_user), repo:BaseCommentRepository = Depends(get_comment_repository)) -> Any:

    comment_service.update_comment(repo, request, current_user)
    response = common_schema.ApiResponse(success=True, message="댓글 업데이트에 성공하였습니다.") 

    return response

@router.get("/{post_id}", response_model=common_schema.ApiResponse)
async def view_list_comment(post_id:str, 
                            current_user: str = Depends(get_current_user), 
                            user_repo:BaseCommentRepository = Depends(get_user_repository),
                            comment_repo:BaseCommentRepository = Depends(get_comment_repository)) -> Any:

    result = comment_service.get_comment_list(user_repo, comment_repo, post_id)

    response = common_schema.ApiResponse[comment_schema.CommentListRes](success=True, message="댓글 조회에 성공하였습니다.", data=result) 
    return response