from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
import logging
import app.model.models as models
from app.repository.base_comment_repository import BaseCommentRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class CommentRepositoryDB(BaseCommentRepository):
    def __init__(self, db:Session):
        super().__init__()
        self.db=db


    def select_comment(self, comment_id:str)->models.Comment:
        stmt = select(models.Comment).where(models.Comment.comment_id == comment_id)
        return self.db.scalar(stmt)

    def insert_comment(self, comment:models.Comment):
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)


    def delete_comment(self, comment_id:str):
        # DELETE FROM Comment WHERE comment_id = :comment_id
        stmt = delete(models.Comment).where(models.Comment.comment_id == comment_id)
        
        result = self.db.execute(stmt)
        self.db.commit()


    def update_comment(self, comment:models.Comment):
        updated_comment = self.db.merge(comment)
        self.db.commit()
    

    def select_comment_list(self, post_id:str)->list[models.Comment]:
        """
        해당 게시글(post_id)에 달린 모든 댓글을 작성 시간 순서대로 조회합니다.
        """
        stmt = (
            select(models.Comment)
            .where(models.Comment.post_id == post_id)
            .order_by(models.Comment.create_time.asc()) # 오래된 댓글부터(오름차순) 정렬
        )
        
        # scalars().all()은 결과를 리스트 형태로 반환합니다.
        return list(self.db.scalars(stmt).all())

    def select_comment_cnt(self, post_id:str)->int:
        stmt = select(func.count()).select_from(models.Comment).where(
            models.Comment.post_id == post_id
        )
        
        return self.db.scalar(stmt) or 0
