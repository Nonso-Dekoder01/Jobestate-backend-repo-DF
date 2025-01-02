from datetime import datetime,timedelta
import os

from fastapi import HTTPException
import jwt

from errors import raise_error
from src.auth.schemas import DataInToken

class TokenService:
    @staticmethod
    async def create_access_token(data: DataInToken, expires_delta: timedelta = timedelta(minutes=2880)):
        try:
            SECRET_KEY = os.getenv('SECRET_KEY')

            expires = datetime.now() + expires_delta
            data.user.id_ = str(data.user.id_)
            data.exp = expires
            return jwt.encode(data.model_dump(), SECRET_KEY, algorithm="HS256")
        except Exception as exc:
            raise_error(exc)
        
    
    @staticmethod
    def decode_token(token: str):
        try:
            SECRET_KEY = os.getenv('SECRET_KEY')
            payload = jwt.decode(token.split(" ")[-1], SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")