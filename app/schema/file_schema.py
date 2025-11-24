from pydantic import BaseModel
from fastapi import UploadFile

###### Request #####
class FileDownloadReq(BaseModel):
    file_id:str

###### Response #####

class FileUploadRes(BaseModel):
    file_id:str

class FileDownloadRes(BaseModel):
    file_url:str