from fastapi import APIRouter,FastAPI, Request
from fastapi.exceptions import RequestValidationError

from config.db import Base, engine
from errors import validation_exception_handler
from src.auth.routers import auth_router
from src.jobs.routers import jobs_router, job_categories_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app_router = APIRouter(prefix="/api")

app_router.include_router(auth_router, tags=["Authentication"])
app_router.include_router(jobs_router, tags=["Jobs"])
app_router.include_router(job_categories_router, tags=["Job Categories"])


app.include_router(app_router)

# To handle parsing errors from request bodies
@app.exception_handler(RequestValidationError)
async def validation_exception_handler_main(request:Request, exc: RequestValidationError):
    return validation_exception_handler(exc)


app.get("/")(lambda:{"message":"Welcome to the job state API"})

# To start, you can use
# python main.py or
# uvicorn main:app --reload --port=8987 --reload --workers=3
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",host="0.0.0.0",port=8987, reload=True)
