from fastapi import BackgroundTasks, Depends

from config.db import get_db
from errors import parse_error

from src.auth.services import AuthService
from src.auth.schemas import (
    LoginSchema, 
    RegisterSchema
)

from response import Response

class AuthController:
    @staticmethod
    async def google_auth():
        """
            Returns the links for to direct the user to login with google
            on the web
        """
        try:
            login_url = await AuthService.login_google()
            return Response(
                login_url,
                message="Url for google auth"
            )
        except Exception as exc:
            return parse_error(exc)
        
    
    @staticmethod
    async def verify_user(
        code: str,
        db = Depends(get_db)
    ):
        try:
            google_user_auth = await AuthService.verify_user(code,db)
            return Response(
                google_user_auth,
            )
        except Exception as exc:
            return parse_error(exc)
        
    
    @staticmethod
    async def signup(
        payload: RegisterSchema,
        background_tasks: BackgroundTasks,
        db = Depends(get_db)
    ):
        """
            Sign up with email and password
        """
        try:
            signup_data = await AuthService.signup(payload, background_tasks, db)
            return Response(
                signup_data,
            )
        except Exception as exc:
            return parse_error(exc)
        
    
    @staticmethod
    async def login(
        payload: LoginSchema,
        db = Depends(get_db)
    ):
        try:
            login_data = await AuthService.login(payload, db)
            return Response(
                login_data
            )
        except Exception as exc:
            return parse_error(exc)