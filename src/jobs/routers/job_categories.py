
from fastapi import APIRouter

from src.jobs.controllers import JobCategoriesController

jobs_router = APIRouter(prefix="/jobs/categories")
controller = JobCategoriesController()


jobs_router.get("")\
	(controller.get)


# jobs_router.get("/{job_id}")\
# 	(controller.find_by_id)


jobs_router.post("")\
	(controller.create)


