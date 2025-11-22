import pandas as pd
import os
from abc import ABC, abstractmethod
from app.model.models import User

class BaseUserRepository(ABC):
    @abstractmethod
    def select_user(self, user_id:str)->User:
        pass
    @abstractmethod
    def insert_user(self, user: User):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass

    @abstractmethod
    def update_user(self, user: User):
        pass

    @abstractmethod
    def update_password(self, new_password:str, user_id:str):
        pass

    @abstractmethod
    def select_user_profile(self, user_id:str)->str:
        pass
