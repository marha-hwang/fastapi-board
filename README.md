
# FastAPI Community Board Project

FastAPI를 활용하여 개발된 커뮤니티 게시판 및 AI 채팅 서버 프로젝트입니다.
사용자 인증, 게시글/댓글 관리, 파일 업로드, 그리고 LLM 기반의 AI 채팅 기능을 제공합니다.

## 🛠 Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Package Manager**: Poetry
- **Database**: MySQL (PyMySQL), SQLAlchemy (ORM)
- **Authentication**: JWT (python-jose)
- **AI/LLM**: OpenAI Async Client (Compatible with vLLM)
- **Tools**: Pandas, Uvicorn

## ✨ Key Features

1.  **회원 관리 (User Management)**
    -   회원가입, 로그인 (JWT 인증)
    -   사용자 프로필 관리

2.  **게시판 (Board System)**
    -   게시글 작성, 조회, 수정, 삭제 (CRUD)
    -   댓글 작성 및 관리
    -   조회수 및 좋아요 기능

3.  **파일 관리 (File Management)**
    -   이미지 업로드 및 정적 파일 서빙 (`/images`)

4.  **AI 채팅 (AI Chat)**
    -   OpenAI API 호환 인터페이스를 통한 LLM 연동
    -   스트리밍 답변 지원 (SSE - Server Sent Events)

## 📂 Project Structure

```bash
fastapi-app/
├── app/
│   ├── core/           # 예외 처리 및 핵심 로직
│   ├── model/          # 데이터베이스 모델 (SQLAlchemy)
│   ├── repository/     # DB 접근 계층 (CRUD)
│   ├── routes/         # API 라우터 (Auth, User, Post, Comment, File)
│   ├── schema/         # Pydantic 스키마 (Request/Response DTO)
│   ├── service/        # 비즈니스 로직
│   ├── config.py       # 설정 관리
│   └── main.py         # 앱 진입점
├── images/             # 업로드된 이미지 저장소
├── settings.toml       # 서버 및 모델 설정 파일
├── pyproject.toml      # 의존성 및 프로젝트 설정
└── README.md           # 프로젝트 문서
```

## 🚀 Getting Started

### 1. 환경 설정 (Prerequisites)

Conda 가상환경을 생성하고 활성화합니다.

```bash
# 파이썬 가상환경 생성
conda create --name my_fastapi_env python=3.12

# 파이썬 가상환경 활성화
conda activate my_fastapi_env
```

### 2. 의존성 설치 (Installation)

Poetry를 사용하여 프로젝트 의존성을 설치합니다.

```bash
# Poetry 설치
pip install poetry

# Conda 환경 사용 시 가상환경 생성 비활성화 설정
poetry config virtualenvs.create false

# 의존성 설치 (pyproject.toml 기반)
poetry install
```

### 3. 데이터베이스 및 설정 (Configuration)

`settings.toml` 파일에서 서버 설정을 확인할 수 있습니다.
데이터베이스 연결 설정은 `app/config.py` 또는 환경 변수를 통해 관리됩니다. (실제 DB 연결 정보 확인 필요)

### 4. 서버 실행 (Run Server)

Uvicorn을 사용하여 FastAPI 서버를 실행합니다.

```bash
# 개발 모드로 서버 실행 (코드 변경 시 자동 재시작)
poetry run uvicorn app.main:app --reload --port 8001
```

서버가 실행되면 다음 주소에서 API 문서를 확인할 수 있습니다:
- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **ReDoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)

## 📑 Documentation

### UI 설계서 (Figma)
[Figma Link](https://www.figma.com/file/uzVLRNRe4ocdIjr7xegIuf/%EA%B5%90%EC%9E%AC%EC%9A%A9-%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0-%EC%9B%B9?type=design&node-id=0%3A1&mode=design&t=7fImiK3c25slLqRw-1)

### REST API 설계서 (Google Sheets)
[API Design Link](https://docs.google.com/spreadsheets/d/1sFKSmkjUNMr6xyfy5WnViJ0tmjlPTwENiLvQ0qHtTZM/edit?gid=1878554884#gid=1878554884)
