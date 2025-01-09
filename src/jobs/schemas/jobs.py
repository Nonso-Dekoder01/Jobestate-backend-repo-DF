from typing import List,Optional
from pydantic import BaseModel

from src.jobs.enums import JobTypes, SalaryPeriod

class JobCreate(BaseModel):
	title: str
	description: str
	minimum_salary: float
	maximum_salary: float
	company_name: str
	job_type: JobTypes
	salary_period: SalaryPeriod
	job_category_ids: List[int]


class JobCategoryCreate(BaseModel):
	name: str


class JobsUpdate(BaseModel):
	pass
