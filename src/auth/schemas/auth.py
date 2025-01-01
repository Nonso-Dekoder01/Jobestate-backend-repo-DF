from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    """
        Schema for user to login
    """
    email: str
    password: str


class RegisterSchema(BaseModel):
    email: str
    phone_number: str
    password: str

    # NOTE: As of right now,
    # I'm not sure if the following fields will be required on signup
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    