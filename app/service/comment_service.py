import app.schema.comment_schema as comment_schema
import app.model.models as models
import app.core.security as security
from app.repository.base_comment_repository import BaseCommentRepository
from app.repository.base_user_repository import BaseUserRepository
import logging
from app.core.exception import CustomException, ErrorCode
import app.core.util as util


logger = logging.getLogger(__name__)

def create_comment(repo:BaseCommentRepository ,data: comment_schema.CommentCreateReq, user_id:str)->str :

    # Post model객체 생성하여 crud 수행
    new_comment_id = util.generate_random_string()
    comment = models.Comment(
        comment_id=new_comment_id,
        post_id=data.post_id,
        user_id=user_id,
        content=data.comment,
        create_time=util.get_current_time_string()
    )

    try :
        repo.insert_comment(comment)
    except Exception as e:
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="댓글 작성에 실패하였습니다.")

def remove_comment(repo:BaseCommentRepository ,data:comment_schema.CommentDeleteReq, user_id:str)->str :

    comment = repo.select_comment(data.comment_id)
    if comment == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="해당 댓글이 존재하지 않습니다.")

    if comment.user_id != user_id : 
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="자신이 작성한 댓글만 삭제 가능합니다.")

    try :
        repo.delete_comment(data.comment_id)
    except :
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="댓글 삭제에 실패하였습니다." )
    

def update_comment(repo:BaseCommentRepository ,data:comment_schema.CommentUpdateReq, user_id:str)->str :
    
    comment = repo.select_comment(data.comment_id)

    if comment == None :
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="해당 댓글이 존재하지 않습니다.")

    if comment.user_id != user_id : 
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="자신이 작성한 댓글만 삭제 가능합니다.")

    comment.content = data.comment

    try :
        repo.update_comment(comment)
    except :
        logger.error("error", exc_info=True)
        raise CustomException(code=ErrorCode.INVALID_INPUT_VALUE, message="댓글 업데이트에 실패하였습니다." )


def get_comment_list(user_repo:BaseUserRepository, comment_repo:BaseCommentRepository, post_id:str)->comment_schema.CommentListRes :

    comment_list:list[models.Comment] = comment_repo.select_comment_list(post_id)
    if comment_list == None or len(comment_list) == 0 :
        return comment_schema.CommentListRes(comments=[])

    comment_res = []
    for comment in comment_list:
        user = user_repo.select_user(comment.user_id)
        profile_id = user.img_id if user != None else None
        comment_res.append(
            comment_schema.Comment(
                comment_id=comment.comment_id,
                content=comment.content,
                user_id=comment.user_id,
                profile_id=profile_id if profile_id != None else "",
                create_time=str(comment.create_time)
            )
        )
    result = comment_schema.CommentListRes(comments=comment_res)
    return result