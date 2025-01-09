
from fastapi import APIRouter

from src.jobs.controllers import JobCategoriesController

jobs_router = APIRouter(prefix="/jobs/categories")


jobs_router.get("")\
	(JobCategoriesController.get_all_jobs)


# jobs_router.get("/{job_id}")\
# 	(controller.find_by_id)


jobs_router.post("")\
	(JobCategoriesController.create)


