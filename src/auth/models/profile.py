from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, String ,UUID
from sqlalchemy.orm import relationship
from config.db import Base


class EmployerProfile(Base):
    __tablename__ = "employer_profile"

    id_ = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id_"), nullable=False)
    user = relationship("User", back_populates="employer_profile")

    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    company_website = Column(String, nullable=False)
    location = Column(String, nullable=False)
    about_us = Column(String, nullable=False)

    date_added = Column(DateTime, default=datetime.now)