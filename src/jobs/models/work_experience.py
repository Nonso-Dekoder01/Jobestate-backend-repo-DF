from datetime import datetime
from uuid import uuid4
from sqlalchemy import  Column, Date, ForeignKey, String ,UUID
from sqlalchemy.orm import relationship
from config.db import Base


class WorkExperience(Base):
    __tablename__ = "work_experience"

    id_ = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id_"), nullable=False)
    user = relationship("User", back_populates="work_experiences")

    
    job_role = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    duration = Column(String, nullable=False)
    job_description = Column(String, nullable=True)
    date_added = Column(Date, default=datetime.now)
