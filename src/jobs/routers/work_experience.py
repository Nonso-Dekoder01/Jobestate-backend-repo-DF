from fastapi import APIRouter

from src.jobs.controllers import WorkExperienceController

work_experience_router = APIRouter(prefix="/work-experience")
controller = WorkExperienceController()

work_experience_router.get("")\
    (controller.get_all_user_work_experience)

work_experience_router.post("")\
    (controller.add_work_experience)

work_experience_router.delete("/{work_experience_id}")\
    (controller.remove_work_experience)