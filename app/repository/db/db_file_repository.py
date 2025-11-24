from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func
import logging
import app.model.models as models
from app.repository.base_file_repository import BaseFileRepository
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class FileRepositoryDB(BaseFileRepository):

    def __init__(self, db:Session):
        super().__init__()
        self.db=db
        
    def select_file(self, img_id:str)->models.File:
        stmt = select(models.File).where(
            models.File.img_id == img_id
        )
        return self.db.scalar(stmt)

    def insert_file(self, file:models.File):
        self.db.add(file)
        self.db.commit()