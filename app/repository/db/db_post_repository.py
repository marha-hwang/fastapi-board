from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
import logging
import app.model.models as models
from app.repository.base_post_repository import BasePostRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class PostRepositoryDB(BasePostRepository):
    def __init__(self, db:Session):
        super().__init__()
        self.db=db

    def select_post(self, post_id:str)->models.Post:
        # SELECT * FROM Post WHERE post_id = :post_id
        stmt = select(models.Post).where(models.Post.post_id == post_id)
        return self.db.scalar(stmt)

    def insert_post(self, post:models.Post):
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post) # DB에 저장된 후 생성된 정보(create_time 등) 갱신

    def delete_post(self, post_id:str):
        post = self.select_post(post_id)
        self.db.delete(post)
        self.db.commit()

    def update_post(self, post:models.Post):
        # merge를 사용하여 Detached 상태의 객체도 안전하게 업데이트
        updated_post = self.db.merge(post)
        self.db.commit()

    def increase_view_post_cnt(self, post_id:str):
        stmt = (
            update(models.Post)
            .where(models.Post.post_id == post_id)
            .values(view_cnt=models.Post.view_cnt + 1)
        )
        self.db.execute(stmt)
        self.db.commit()

    def select_post_all(self)->list[models.Post]:
        stmt = (
            select(models.Post)
            .order_by(models.Post.create_time.asc()) 
        )
    
        # scalars().all()은 결과를 리스트 형태로 반환합니다.
        return list(self.db.scalars(stmt).all())

