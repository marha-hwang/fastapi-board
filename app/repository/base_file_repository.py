from abc import ABC, abstractmethod
from app.model.models import File

class BaseFileRepository(ABC):
    @abstractmethod
    def insert_file(self, file:File):
        pass
    @abstractmethod
    def select_file(self, img_id:str)->File:
        pass