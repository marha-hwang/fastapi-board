2. FastAPI로 Route, controller 만 이용해서 구현 후 Postman 요청에 응답하는 커뮤니티 백엔드를 구현해보세요 
  ([커뮤니티](https://www.figma.com/file/uzVLRNRe4ocdIjr7xegIuf/%EA%B5%90%EC%9E%AC%EC%9A%A9-%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0-%EC%9B%B9?type=design&node-id=0%3A1&mode=design&t=7fImiK3c25slLqRw-1))

    2-1. 우선 route 만 이용해서 요청에 응답하는 백엔드를 구현한다.
    2-2. route/controller로 구분하여서 요청에 응답하는 백엔드를 구현한다.
    2-3. 커뮤니티에 맞는 백엔드로 변환한다.

3. (중급자를 위한) 커뮤니티 서비스 HTTP REST API 사전 설계하여 작성해보기 (복제용 rest api 시트 )

4. FastAPI로 Route - Controller - Model 패턴을 적용한 커뮤니티 백엔드를 구현해 보세요.
4-1. Model 코드는 JSON으로만 반환하기 (DB 사용하지 않음)


(필수조건) Postman으로 어떠한 요청을 보내던 예외처리가 잘 되어있어야 함


요구사항 정의
https://docs.google.com/spreadsheets/d/1sFKSmkjUNMr6xyfy5WnViJ0tmjlPTwENiLvQ0qHtTZM/edit?gid=1878554884#gid=1878554884


로그인 기능
로그인 -> 토큰 발급 -> 요청마다 토큰을 포함하여 발송
어떻게 포함시킴??
- Depends(get_current_user)을 통해 토큰 검증
- Depends(oauth2_scheme) : oauth2_scheme 
  -  OAuth2PasswordBearer(tokenUrl="auth/login") : 클라이언트의 요청이 들어오면 토큰 값을 자동으로 추출하여 전달
  - 스웨거에서 form을 사용하지 않고 구현하는 방법은?

1. 프로젝트 구조 정의
2. login, logout기능 구현
3. 파일 + pandas를 통한 db구현

4. 중간 코드 정리

리팩토링 사항
- 데이터 조회시 csv -> db로 변경 가능하도록 인터페이스 사용
- Router생성시 인증로직을 모두 공통으로 처리하도록 변경