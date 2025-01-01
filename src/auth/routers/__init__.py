from fastapi import APIRouter

from src.auth.controllers import AuthController


auth_router = APIRouter(prefix="/auth")

auth_router.get("")\
    (AuthController.google_auth)

auth_router.post("/signup")\
    (AuthController.signup)

auth_router.post("/login")\
    (AuthController.login)

auth_router.get("/google")\
    (AuthController.verify_user)