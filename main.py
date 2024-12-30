from fastapi import APIRouter,FastAPI

from config.db import Base, engine
from src.auth.routers import auth_router

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app_router = APIRouter(prefix="/api")
app_router.include_router(auth_router)

app.include_router(app_router)

# To start, you can use
# python main.py or
# uvicorn main:app --reload --port=8987 --reload --workers=3
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0",port=8987, reload=True)
