

## 프로젝트 개요

- fastapi를 활용한 게시판 만들기



## UI설계서

https://www.figma.com/file/uzVLRNRe4ocdIjr7xegIuf/%EA%B5%90%EC%9E%AC%EC%9A%A9-%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0-%EC%9B%B9?type=design&node-id=0%3A1&mode=design&t=7fImiK3c25slLqRw-1



## REST API설계서

https://docs.google.com/spreadsheets/d/1sFKSmkjUNMr6xyfy5WnViJ0tmjlPTwENiLvQ0qHtTZM/edit?gid=1878554884#gid=1878554884



## 프로젝트 실행방법

### conda 가상환경 생성 및 활성화

```python
# 파이썬 가상환경 생성
conda create --name my_fastapi_env python=3.12
# 파이썬 가상환경 활성화
conda activate my_fastapi_env   
```

### poetry 설치

```python
# 가상환경 내부에서 pip를 통해 poetry설치
pip install poetry

# poetry는 기본적으로 자체 가상환경을 만들려고 시도함
# conda 를 사용하는 환경에서는 이를 비활성화 하도록 설정이 필요
poetry config virtualenvs.create false 
```

### 프로젝트 초기화

```python
# pyproject.toml파일 기반으로 필요한 의존성 다운로드
# pyproject.toml파일을 통해 프로젝트 초기화
# 결과로 lock파일이 자동으로 생성됨
poetry install  
poetry update

```

### fast api 서버 실행

```python
# uvicorn서버를 통해 백엔드 서버 실행
poetry run uvicorn app.main:app --reload --port 8001
```
