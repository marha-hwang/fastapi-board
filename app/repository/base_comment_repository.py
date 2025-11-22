from abc import ABC, abstractmethod
from app.model.models import Comment

class BaseCommentRepository(ABC):
    @abstractmethod
    def select_comment(self, comment_id:str)->Comment:
        pass
    @abstractmethod
    def insert_comment(self, comment:Comment):
        pass
    @abstractmethod
    def delete_comment(self, comment_id:str):
        pass
    @abstractmethod
    def update_comment(self, comment:Comment):
        pass
    @abstractmethod
    def select_comment_list(self, post_id:str)->list[Comment]:
        pass
    @abstractmethod
    def select_comment_cnt(self, post_id:str)->int:
        pass