from typing import List,Optional
from pydantic import BaseModel

from src.jobs.enums import JobTypes, SalaryPeriod

class JobCreate(BaseModel):
	"""
		Schema to create a job
	"""
	title: str
	description: str
	responsibility: str
	qualifications: List[str]
	minimum_salary: float
	maximum_salary: float
	company_name: str
	job_type: JobTypes
	salary_period: SalaryPeriod
	job_category_ids: List[int]


class JobCategoryCreate(BaseModel):
	"""
		Schema to create a job category
	"""
	name: str


class JobsUpdate(JobCreate):
	"""
		Schema to update a job
	"""
	title: Optional[str] = None
	description: Optional[str] = None
	minimum_salary: Optional[str] = None
	maximum_salary: Optional[str] = None
	company_name: Optional[str] = None
	job_type: Optional[str] = None
	salary_period: Optional[SalaryPeriod] = None
	job_category_ids: Optional[List[int]] = None
