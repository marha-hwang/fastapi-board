import pandas as pd
import os
from abc import ABC, abstractmethod
from app.model.models import Post

class BasePostRepository(ABC):
    @abstractmethod
    def select_post(self, post_id:str)->Post:
        pass
    @abstractmethod
    def insert_post(self, post:Post):
        pass
    @abstractmethod
    def delete_post(self, post_id:str):
        pass
    @abstractmethod
    def update_post(self, post:Post):
        pass
    @abstractmethod
    def increase_view_post_cnt(self, post_id:str):
        pass
    @abstractmethod
    def select_post_all(self)->list[Post]:
        pass

    
