from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.auth.schemas.user import CreateUser
from src.auth.models import User

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
            raise exc
        

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
            raise exc
    
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
            raise exc
        

    
    @staticmethod
    async def create(
        payload: CreateUser,
        db: Session
    ):
        try:
            user = User(**payload.model_dump())

            db.add(user)
            db.commit()
            db.refresh(user)

            return user
        except Exception as exc:
            db.rollback()
            raise exc