from uuid import uuid4
from sqlalchemy import UUID, Column, ForeignKey, String, Float, Enum, Integer
from config.db import Base
from src.jobs.enums import JobTypes, SalaryPeriod, JobStatus
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"

    id_ = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    minimum_salary = Column(Float, nullable=True)
    maximum_salary = Column(Float, nullable=True)
    company_name = Column(String(255), nullable=False)
    
    job_type = Column(Enum(JobTypes, name="job_types"), nullable=False) 
    salary_period = Column(Enum(SalaryPeriod, name="salary_period"), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.ACTIVE)
    job_categories = relationship("JobCategory", secondary="job_categories_association", back_populates="jobs")

    

class JobCategory(Base):
    __tablename__ = "job_categories"
    
    id_ = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    jobs = relationship("Job", secondary="job_categories_association", back_populates="job_categories")
    

class JobCategoryAssociation(Base):
    __tablename__ = "job_categories_association"

    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id_"), primary_key=True)
    job_category_id = Column(Integer, ForeignKey("job_categories.id_"), primary_key=True)