import app.model.models as app_models
import app.core.security as security
import app.core.util as util
import logging
import app.crud.comment_crud as comment_crud
import app.schema.comment_schema as comment_schema


logger = logging.getLogger(__name__)

def create_comment(input: comment_schema.CommentCreateReq, user_id:str)->str :

    # Post model객체 생성하여 crud 수행
    new_comment_id = util.generate_random_string()
    comment = app_models.Comment(
        comment_id=new_comment_id,
        post_id=input.post_id,
        user_id=user_id,
        content=input.comment,
        create_time=util.get_current_time_string()
    )

    if comment_crud.insert_comment(comment=comment) : return "댓글 작성에 성공하였습니다."
    else : return "댓글 작성에 실패하였습니다."

def remove_comment(input:comment_schema.CommentDeleteReq, user_id:str)->str :

    comment = comment_crud.select_comment(comment_id=input.comment_id)
    if comment == None : return "해당 댓글이 존재하지 않습니다."
    if comment.user_id != user_id : return "자신이 작성한 댓글만 삭제 가능합니다."

    if comment_crud.delete_comment(comment_id=input.comment_id) : return "댓글 삭제가 성공적으로 완료되었습니다."
    else : return "댓글 삭제에 실패하였습니다." 


def update_comment(input:comment_schema.CommentUpdateReq, user_id:str)->str :
    
    comment:app_models.Comment = comment_crud.select_comment(comment_id=input.comment_id)
    if comment == None : return "해당 댓글이 존재하지 않습니다."
    if comment.user_id != user_id : return "자신이 작성한 댓글만 삭제 가능합니다."

    # Post model객체 생성하여 crud 수행
    comment.content = input.comment

    if comment_crud.update_comment(comment=comment) : return "댓글 업데이트가 성공적으로 완료되었습니다."
    else : return "댓글 업데이트에 실패하였습니다."


def get_comment_list(post_id:str)->comment_schema.CommentListRes :

    comment_list = comment_crud.select_comment_list(post_id=post_id)
    if comment_list == None : return None
    return comment_list