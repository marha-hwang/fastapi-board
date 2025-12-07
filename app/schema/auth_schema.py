from pydantic import BaseModel, Field, field_validator

class Login(BaseModel):
    # pydantic는 필수값이 없는 경우 기본에러를 뱉음
    # 기본에러가 아닌 커스텀된 에러를 사용하고 싶다면 @validator을 사용해야 함
    # 필드를 아예 안 보내면 validator을 아예 실행하지 않음
    # 따라서 None이 들어가게 해서, 일단 Pydantic의 1차 검문을 통과시켜야 함
    user_id:str | None = None
    password:str | None = None

    @field_validator('user_id')
    @classmethod
    def check_userId_required(cls, v: str | None) -> str:
        if v is None:
            raise ValueError("ID는 필수 입력 항목입니다.")
        
        if "@" not in v:
            raise ValueError("ID 형식이 올바르지 않습니다.")
        
        return v
    @field_validator('password')
    @classmethod
    def check_password_required(cls, v: str | None) -> str:
        if v is None:
            raise ValueError("비밀번호는 필수 입력 항목입니다.")
        
        if len(v) < 8:
            raise ValueError("비밀번호는 8자리 이상이어야 합니다.")
        
        return v

class UserInfo(BaseModel):
    user_id:str
    nickname:str
    img_id:str | None = ""

class LoginResponse(BaseModel):
    access_token : str
    token_type : str
    user : UserInfo