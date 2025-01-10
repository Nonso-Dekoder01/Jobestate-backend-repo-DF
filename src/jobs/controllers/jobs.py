from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.db import get_db
from errors import parse_error

from response import Response
# from src.auth.services import UserService
from src.jobs.schemas import (
    JobCreate,
	JobsUpdate
)
from src.jobs.services import JobsService


class JobsController:
	
	@staticmethod
	async def get_all_jobs(db = Depends(get_db)):
		try:
			jobs = await JobsService.get(db)
			return Response(jobs, message="All jobs")
		except Exception as exc:
			return parse_error(exc)

	@staticmethod
	async def find_by_id(job_id:UUID, db = Depends(get_db)):
		try:
			job = await JobsService.find(job_id,db)
			return Response(
				job
			)
		except Exception as exc:
			return parse_error(exc)


	@staticmethod
	async def update(
		job_id: UUID,
		payload: JobsUpdate,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
		db = Depends(get_db)
		):
		"""
			Update a job
		"""
		try:
			updated_job = await JobsService.update(
				job_id,
				payload,
				db
			)

			return Response(updated_job)
		except Exception as exc:
			return parse_error(exc)


	@staticmethod
	async def create(
		payload: JobCreate,
		db = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
		# user = Depends(UserService.check_admin_token)
	):
		"""
			Creates a new job 
			Below are the specified parameters
		"""
		try:
			job = await JobsService.create(payload,db)
			return Response(
				job,
				message="New job added"
			)
		except Exception as exc:
			return parse_error(exc)


	@staticmethod
	async def delete( 
		job_id: UUID, 
		db=Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
		):
		"""
			Delete a job 
		"""
		try:
			await JobsService.delete(job_id,db)
			return Response(message="Job deleted")
		except Exception as exc:
			return parse_error(exc)
