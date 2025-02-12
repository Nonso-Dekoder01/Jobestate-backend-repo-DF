from fastapi import APIRouter

from src.jobs.controllers import EducationController

education_router = APIRouter(prefix="/education")
controller = EducationController()

education_router.get("")\
    (controller.get_all_user_education)

education_router.post("")\
    (controller.add_education)

education_router.delete("/{education_id}")\
    (controller.remove_education)