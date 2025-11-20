from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success:bool = Field(default=None, description="응답상태")
    code:str = Field(default=None, description="응답 코드")
    message:str = Field(default=None, description="응답 메시지")
    data: T | None = Field(default=None, description="응답 데이터 페이로드")

'''
pydantic에서 필요한 기능은?
    기본값 처리 : x:str = "str"
    선택값 처리 : x:str | None = None
    제약조건, 유효성 검증 : 기본값과 선택값이 존재하는 상태에서 제약조건을 걸고 싶으면 Field사용
    조건에 맞지 않는 경우 에러처리 방식 : @validator을 사용하여 원하는 에러 발생시키기 가능
'''

'''
응답코드 구성은 어떻게 할 것인가?
    대분류 : HTTP상태코드 숫자 이용,ex) 클라이언트, 서버, 권한문제 분류
    body code : 문자코드 이용,
         과거에는 성능으로 숫자코드를 이용했지만, 현재는 개발의 편의성을 위해 문자코드를 사용

'''