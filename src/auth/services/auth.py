from os import getenv
import requests

from dotenv import load_dotenv
from jose import jwt
from sqlalchemy.orm import Session


from src.auth.enums import AuthMethods
from src.auth.schemas import (
    CreateUser,
    GoogleOauthUserResponse,
    NewUserFromGoogle
)
from .user import UserService


load_dotenv()
class AuthService:
    @staticmethod
    async def login_google():
        try:
            return {
                "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={getenv('GOOGLE_CLIENT_ID')}&redirect_uri={getenv('GOOGLE_REDIRECT_UR','http://localhost:8987/api/auth/google')}&scope=openid%20profile%20email&access_type=offline"
            }
        except Exception as exc:
            raise exc
        

    
    @staticmethod
    async def google_user_info(code: str):
        try:
            token_url = "https://accounts.google.com/o/oauth2/token"
            
            data = {
            "code": code,
            "client_id": getenv('GOOGLE_CLIENT_ID'),
            "client_secret": getenv('GOOGLE_CLIENT_SECRET'),
            "redirect_uri": getenv('GOOGLE_REDIRECT_UR','http://localhost:8987/api/auth/google'),
            "grant_type": "authorization_code",
            }

            response = requests.post(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
            
            # Possible errors that can occur:
            # - invalid_grant: if the code has been used before
            # - redirect_uri_mismatch: if the redirect_uri is not the same as the one used in the request
            
            access_token = response.json().get("access_token")
            print(response.json())

            user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
            print(user_info.json())
            return GoogleOauthUserResponse(**user_info.json())
        except Exception as exc:
            raise exc
        


    @staticmethod
    async def verify_user(
        code: str,
        db: Session
    ):
        """
            Verifies user by retrieving information from google

            It creates a new user in our database if the user doesn't exist
        """
        try:
            user_info = await AuthService.google_user_info(code)

            #TODO: Check for the user in the database by email
            # and creates the user if they don't exist
            user = await UserService.get_by_email(user_info.email,db)

            if not user:
                user = await UserService.create(
                    CreateUser(
                        first_name=user_info.given_name,
                        last_name=user_info.family_name,
                        email=user_info.email,
                        auth_method=AuthMethods.GOOGLE
                    ),
                    db
                )
            
            return NewUserFromGoogle.model_validate(user)
        except Exception as exc:
            raise exc


    @staticmethod
    async def get_token(token: str):
        try:
            return jwt.decode(token, getenv('GOOGLE_CLIENT_SECRET'), algorithms=["HS256"])
        except Exception as exc:
            raise exc