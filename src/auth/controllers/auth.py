from fastapi import Depends

from config.db import get_db

from src.auth.services import AuthService
from src.auth.schemas import (
    LoginSchema, 
    RegisterSchema
)

class AuthController:
    @staticmethod
    async def google_auth():
        """
            Returns the links for to direct the user to login with google
            on the web
        """
        try:
            return await AuthService.login_google()
        except Exception as exc:
            return str(exc)
        
    
    @staticmethod
    async def verify_user(
        code: str,
        db = Depends(get_db)
    ):
        try:
            return await AuthService.verify_user(code,db)
        except Exception as exc:
            return str(exc)
        
    
    @staticmethod
    async def signup(
        payload: RegisterSchema,
        db = Depends(get_db)
    ):
        """
            Sign up with email and password
        """
        try:
            return await AuthService.signup(payload, db)
        except Exception as exc:
            return str(exc)
        
    
    @staticmethod
    async def login(
        payload: LoginSchema,
        db = Depends(get_db)
    ):
        try:
            return await AuthService.login(payload, db)
        except Exception as exc:
            print(exc)
            return str(exc)