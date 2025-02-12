from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Date, ForeignKey, String ,UUID
from sqlalchemy.orm import relationship
from config.db import Base


class Education(Base):
    __tablename__ = "education"

    id_ = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id_"), nullable=False)
    user = relationship("User", back_populates="education")

    degree = Column(String, nullable=False)
    institution_name = Column(String, nullable=False)
    course = Column(String, nullable=True)

    admission_date = Column(Date, nullable=False)
    completion_date = Column(Date, nullable=False)

    date_added = Column(Date, default=datetime.now)