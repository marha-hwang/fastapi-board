from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
import logging
import app.model.models as models
from app.repository.base_like_repository import BaseLikePostRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class LikeRepositoryDB(BaseLikePostRepository):

    def __init__(self, db:Session):
        super().__init__()
        self.db=db
        
    def select_like(self, post_id:str, user_id:str)->models.PostLike:
        # SELECT * FROM PostLike WHERE post_id = :post_id AND user_id = :user_id
        stmt = select(models.PostLike).where(
            models.PostLike.post_id == post_id,
            models.PostLike.user_id == user_id
        )
        return self.db.scalar(stmt)

    def insert_like(self, post_id:str, user_id:str):
        like = models.PostLike(post_id=post_id, user_id=user_id)
        
        self.db.add(like)
        self.db.commit()

    def delete_like(self, post_id:str, user_id:str):
        stmt = delete(models.PostLike).where(
            models.PostLike.post_id == post_id,
            models.PostLike.user_id == user_id
        )
        
        self.db.execute(stmt)
        self.db.commit()

    def select_like_cnt(self, post_id:str)->int:
        # SELECT COUNT(*) FROM PostLike WHERE post_id = :post_id
        stmt = select(func.count()).select_from(models.PostLike).where(
            models.PostLike.post_id == post_id
        )
        
        # count() 집계 함수의 결과(정수)를 반환
        # 결과가 없으면 0이 반환됩니다.
        return self.db.scalar(stmt) or 0
