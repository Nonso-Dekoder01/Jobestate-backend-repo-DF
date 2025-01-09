from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from errors import raise_error
from src.jobs.schemas import JobCreate
from src.jobs.enums import JobStatus
from src.jobs.models import Job

from .job_categories import JobCategoryService


class JobsService:
	@staticmethod
	async def get_by_id(
			job_id: UUID,
			db: Session
	) -> Job|None:
		try:
			return db.query(Job).filter(Job.id_ == job_id, Job.status.not_in([JobStatus.DELETED])).first()
		except Exception as exc:
			raise_error(exc)


	@staticmethod
	async def get(
		db: Session
	):
		try:
			return db.query(Job).filter(Job.status.not_in([JobStatus.DELETED])).all()
		except Exception as exc:
			raise_error(exc)

	@staticmethod
	async def find(job_id: UUID, db: Session) -> Job:
		try:
			job = await JobsService.get_by_id(job_id,db)
			if not job:
				raise HTTPException(
					404,
					f"Job {job_id} not found"
				)

			return job
		except Exception as exc:
			raise_error(exc)
	

	async def update(job_id):
		pass


	
	async def create(payload: JobCreate,db:Session):
		try:
			job_categories = await JobCategoryService\
				.bulk_find(payload.job_category_ids,db)
			
			job = Job(
				title=payload.title,
				description=payload.description,
				minimum_salary=payload.minimum_salary,
				maximum_salary=payload.maximum_salary,
				company_name=payload.company_name,
				job_type=payload.job_type,
				salary_period=payload.salary_period,
			)

			db.add(job)
			db.commit(job)

			job.job_categories = job_categories
			
			db.refresh(job)

			return job
		except Exception as exc:
			raise_error(exc)


	
	async def delete(job_id:UUID, db: Session):
		try:
			job = await JobsService.find(job_id,db)

			job.status = JobStatus.DELETED
			db.commit()
		except Exception as exc:
			db.rollback()
			raise_error(exc)
