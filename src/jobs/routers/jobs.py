
from fastapi import APIRouter

from src.jobs.controllers import JobsController

jobs_router = APIRouter(prefix="/jobs")
controller = JobsController()


jobs_router.get("")\
	(controller.get_all_jobs)


jobs_router.get("/{job_id}")\
	(controller.find_by_id)




jobs_router.post("")\
	(controller.create)


	

jobs_router.patch("/{job_id}")\
	(controller.update)



jobs_router.delete("/{job_id}")\
	(controller.delete)
