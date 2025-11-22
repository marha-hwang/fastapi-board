from abc import ABC, abstractmethod
from app.model.models import PostLike

class BaseLikePostRepository(ABC):
    @abstractmethod
    def select_like(self, post_id:str, user_id:str)->PostLike:
        pass
    @abstractmethod
    def insert_like(self, post_id:str, user_id:str):
        pass
    @abstractmethod
    def delete_like(self, post_id:str, user_id:str):
        pass
    @abstractmethod
    def select_like_cnt(self, post_id:str)->int:
        pass
