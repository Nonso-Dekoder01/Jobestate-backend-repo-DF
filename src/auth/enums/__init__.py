from enum import Enum


class AuthMethods(str, Enum):
    """
        Methods by which
        a user can be logged onto the 
        platform
    """
    EMAIL_PASSWORD = "email_password"
    GOOGLE = "google"
    # SOCIAL_MEDIA = "social_media"


class Roles(str, Enum):
    """
        Types of roles on the platform
    """
    ADMIN = "admin"
    USER = "user"


class Status(str, Enum):
    """
        Possible status the user's account
        can exist in
    """
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"