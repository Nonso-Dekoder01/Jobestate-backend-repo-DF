from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from src.auth.enums import AuthMethods, Roles


class BaseUserSchema(BaseModel):
    """
        Schema model to create a new user
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone_number: Optional[str] = None
    auth_method: AuthMethods

    class Config:
        from_attributes = True


class CreateUser(BaseUserSchema):
    password: Optional[str] = None


class GoogleOauthUserResponse(BaseModel):
   """
    Response gotten from this [endpoint](https://www.googleapis.com/oauth2/v1/userinfo)
   """

   id: str
   email: str
   verified_email: bool
   name: str
   given_name: str
   family_name: str
   picture: str



class NewUserFromGoogle(BaseUserSchema):
    token: Optional[str] = None
    class Config:
        from_attributes=True



class LoginResponse(BaseModel):
    user: BaseUserSchema
    token: str


class UserSchema(BaseUserSchema):
    id_: UUID | str
    role: Roles
    
    class Config:
        from_attributes=True



class DataInToken(BaseModel):
    user: UserSchema
    exp: Optional[datetime] = None

    class Config: 
        from_attributes = True
