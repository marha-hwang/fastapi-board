from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
import logging
import app.model.models as models
from app.repository.base_user_repository import BaseUserRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class UserRepositoryDB(BaseUserRepository):
    def __init__(self, db:Session):
        super().__init__()
        self.db=db

    def select_user(self, user_id:str)->models.User:
        # SELECT * FROM User WHERE user_id = :user_id
        stmt = select(models.User).where(models.User.user_id == user_id)
        return self.db.scalar(stmt)

    def insert_user(self, user: models.User) :
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user) # DB에서 생성된 값(default 등)을 인스턴스에 반영

    def delete_user(self, user_id: str) :
        user = self.select_user(user_id)
        if user == None : raise Exception()

        self.db.delete(user)
        self.db.commit()

    def update_user(self, user: models.User) :
        # 이미 세션에 포함된 객체라면 commit만으로 반영되지만,
        # 세션에 없는 객체일 경우 merge를 사용합니다.
        updated_user = self.db.merge(user)
        self.db.commit()


    def update_password(self, new_password:str, user_id:str) :
        # UPDATE User SET password = :new_password WHERE user_id = :user_id
        stmt = (
            update(models.User)
            .where(models.User.user_id == user_id)
            .values(password=new_password)
        )
        self.db.execute(stmt)
        self.db.commit()


    def select_user_profile(self, user_id:str)->str:
        stmt = select(models.User.img_id).where(models.User.user_id == user_id)
        profile_url = self.db.scalar(stmt)
        if profile_url : return profile_url
        else : return None