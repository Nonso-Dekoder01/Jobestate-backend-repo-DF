from os import getenv
import os
import random
import requests

from dotenv import load_dotenv
from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from errors import raise_error
from messages.services import EmailService
from src.auth.enums import AuthMethods, Status as UserStatus
from src.auth.schemas import (
    CreateUser,
    DataInToken,
    GoogleOauthUserResponse,
    LoginSchema,
    LoginResponse,
    NewUserFromGoogle,
    RegisterSchema,
    UserSchema
)

from .password import PasswordService
from .user import UserService
from .token import TokenService

load_dotenv()
class AuthService:
    @staticmethod
    async def login_google():
        try:
            google_redirect_uri = getenv('GOOGLE_REDIRECT_URI')
            return {
                "redirect_uri": google_redirect_uri,
                "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={getenv('GOOGLE_CLIENT_ID')}&redirect_uri={getenv('GOOGLE_REDIRECT_URI','http://localhost:8987/api/auth/google')}&scope=openid%20profile%20email&access_type=offline"
            }
        except Exception as exc:
            raise_error(exc)
        

    
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
            raise_error(exc)
        


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
            raise_error(exc)


    # @staticmethod
    # async def get_token(token: str):
    #     try:
    #         return jwt.decode(token, getenv('GOOGLE_CLIENT_SECRET'), algorithms=["HS256"])
    #     except Exception as exc:
    #         raise_error(exc)
        
    
    @staticmethod
    async def signup(
        payload: RegisterSchema,
        background_task: BackgroundTasks,
        db: Session
    ):
        try:
            # user = await UserService.create(
            #     CreateUser(
            #         **payload.model_dump(), 
            #         auth_method=AuthMethods.EMAIL_PASSWORD
            #         ), 
            #     db
            # )

            background_task.add_task(
                AuthService.send_verification_email,
                payload.email
            )
            # return UserSchema.model_validate(user)
        except Exception as exc:
            raise_error(exc)
        
    
    @staticmethod
    async def login(
        payload: LoginSchema,
        db: Session
    ):
        try:
            user = await UserService.find_by_email(payload.email, db)
            if user.auth_method == AuthMethods.GOOGLE:
                raise HTTPException(
                    400,
                    "Login with google instead."
                )
            if user.status != UserStatus.ACTIVE:
                raise HTTPException(
                    403,
                    "This user's account is not active. Please reach out to our customer care if you believe this is an error and you have completed your registration."
                )
            if not PasswordService.check_password(payload.password, user.password):
                raise HTTPException(
                    400,
                    "Incorrect password"
                )
            
            return LoginResponse(
                user=user,
                token=await TokenService.create_access_token(DataInToken(user=UserSchema.model_validate(user)))
            )
        except Exception as exc:
            raise_error(exc)


    
    @staticmethod
    async def send_verification_email(email: str):
        try:
            otp = random.randint(100000,999999)
            
            subject = 'Email Verification'
            
            html_file_path = os.path.join(os.getcwd(), 'messages','templates', 'verification_email.html')
            print(html_file_path)
            with open(html_file_path, 'r') as file:
                message = file.read()
                
            message = message.replace('{{email_six_digits_code}}',str(otp))

            await EmailService.send_email(email, subject, message)
        except Exception as exc:
            raise_error(exc)