from datetime import datetime
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, Enum, String ,UUID
from src.auth.enums import AuthMethods, Roles, Status as UserStatus
from config.db import Base

class User(Base):
    """
        Jobstate user object
    """
    __tablename__ = "users"

    id_ = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    role = Column(Enum(Roles,name="role"), default=Roles.USER)
    phone_number = Column(String)

    password = Column(String, nullable=True)
    auth_method = Column(Enum(AuthMethods, name="auth_method"))

    is_phone_verified = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    status = Column(Enum(UserStatus, name="user_status"), default=UserStatus.PENDING_VERIFICATION)
    created_at = Column(DateTime, default=datetime.now)