from fastapi import FastAPI
from .config import server_config
from app.api.main import api_router

app = FastAPI(title="FastAPI + Poetry AI Server")

@app.get("/")
async def root():
    return {"message": "AI Model Server is running 🚀"}

app.include_router(api_router)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "app.main:app",
#         host=server_config["host"],
#         port=server_config["port"],
#         reload=server_config["reload"]
#     )
