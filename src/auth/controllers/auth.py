from fastapi import Depends
from config.db import get_db
from src.auth.services import AuthService

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