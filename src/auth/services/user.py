from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import or_

from errors import raise_error
from src.auth.enums import Roles, Status as UserStatus
from src.auth.schemas.user import CreateUser, DataInToken
from src.auth.models import User

from .password import PasswordService
from .token import TokenService


class UserService:
    """
        Service class with methods 
        by which the user model may be
        interacted with.
    """


    @staticmethod
    async def find_by_id(
        user_id: UUID,
        db: Session
    ):
        """
            Finds the user by id

            Raises an error if the user is not found
        """
        try:
            user = db.query(User)\
                .filter(User.id_ == user_id).first()
            
            if not user:
                raise HTTPException(404,f"User {user_id} not found")
            
            return user
        except Exception as exc:
            raise_error(exc)
        

    @staticmethod
    async def get_by_email(
        email: str,
        db: Session
    ):
        """
            Checks the database to see
            if a user with the email address exists.
            
            Returns None if the user is not found.
        """
        try:
            return db.query(User)\
                .filter(User.email == email).first()
        except Exception as exc:
            raise_error(exc)
    
    @staticmethod
    async def find_by_email(
        email: str,
        db: Session
    ):
        """
            Finds the user by email

            Raises an error if the user is not found
        """
        try:
            user = await UserService.get_by_email(email,db)
            
            if not user:
                raise HTTPException(
                    404,
                    f"User with email {email} not found"
                )
            
            return user
        except Exception as exc:
            raise_error(exc)
        

    async def get_user(
        email: str|None,
        phone_number: str|None,
        db: Session
    ):
        """
            Checks the database to see if the user exists.
        """
        try:
            return db.query(User).filter(or_(User.email == email, User.phone_number == phone_number)).first()
        except Exception as exc:
            raise_error(exc)
    
    @staticmethod
    async def create(
        payload: CreateUser,
        db: Session
    ):
        try:
            existing_user = await UserService.get_user(
                payload.email,
                payload.phone_number,
                db
            )
            if existing_user:
                raise HTTPException(
                    400,
                    "This user already exists"
                )
            
            user = User(**payload.model_dump())

            if payload.password:
                password = PasswordService.hash_password(payload.password)
                user.password = password.decode("utf-8")
            user.status = UserStatus.ACTIVE

            db.add(user)
            db.commit()
            db.refresh(user)

            return user
        except Exception as exc:
            db.rollback()
            raise_error(exc)
        
    
    @staticmethod
    async def is_admin(
        user_id: UUID,
        db: Session
    ):
        """
            Checks if a user is an admin or not
            and returns a boolean to that effect.
        """
        try:
            user = await UserService.find_by_id(user_id, db)

            if user.role == Roles.ADMIN:
                return True
            
            return False
        except Exception as exc:
            raise_error(exc)
        

    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ):
        try:
            return DataInToken.model_validate(TokenService.decode_token(credentials.credentials))
        except Exception as exc:
            raise_error(exc)
        
    
    @staticmethod
    async def check_admin_token(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ):
        try:
            user = await UserService.get_current_user(credentials)
            if user.user.role != Roles.ADMIN:
                raise HTTPException(
                    401,
                    f"You must be an admin to perform this task"
                )
        except Exception as exc:
            raise_error(exc)