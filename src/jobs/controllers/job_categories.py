from fastapi import Depends

from config.db import get_db
from errors import parse_error
from response import Response
from src.jobs.services import JobCategoryService
from src.jobs.schemas import JobCategoryCreate


class JobCategoriesController:
    @staticmethod
    async def create(
        payload: JobCategoryCreate,
        db = Depends(get_db)
    ):
        try:
            job_category = await JobCategoryService.create(payload,db)

            return Response(job_category)
        except Exception as exc:
            return parse_error(exc)
        
    @staticmethod
    async def get_all_jobs(
        db = Depends(get_db)
    ):
        try:
            job_categories = await JobCategoryService.get_all(db)

            return Response(job_categories)
        except Exception as exc:
            return parse_error(exc)
    

    
    