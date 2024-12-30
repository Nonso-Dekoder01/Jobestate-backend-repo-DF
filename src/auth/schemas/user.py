from typing import Optional
from pydantic import BaseModel

from src.auth.enums import AuthMethods


class BaseUserSchema(BaseModel):
    """
        Schema model to create a new user
    """
    first_name: str 
    last_name: str
    email: str
    phone_number: Optional[str] = None
    auth_method: AuthMethods


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
    class Config:
        from_attributes=True