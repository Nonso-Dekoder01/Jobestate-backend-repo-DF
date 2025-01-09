from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from errors import raise_error
from src.jobs.models import JobCategory
from src.jobs.schemas import JobCategoryCreate


class JobCategoryService:
    @staticmethod
    async def get_all(
        db: Session
    ):
        try:
            return db.query(JobCategory).all()
        except Exception as exc:
            raise_error(exc)


    @staticmethod
    async def find_by_id(
        job_category_id: int,
        db: Session,
    ):
        try:
            job_category = db.query(JobCategory)\
                .filter(JobCategory.id_ == job_category_id).first()
            
            if not job_category:
                raise HTTPException(
                    404,
                    f"Job category not found"
                )
            
            return job_category
        except Exception as exc:
            raise_error(exc)
        
    
    @staticmethod
    async def bulk_find(
        job_category_ids: List[int],
        db: Session
    ):
        try:
            job_categories = []

            for job_category_id in job_category_ids:
                job_categories.append(await JobCategoryService.find_by_id(job_category_id, db))
            
            return job_categories
        except Exception as exc:
            raise_error(exc)


    @staticmethod
    async def find_by_name(
        name: str,
        db: Session
    ):
        try:
            job = db.query(JobCategory).filter_by(name=name.capitalize().strip()).first()

            if not job:
                raise HTTPException(
                    404,
                    f"Job {name} not found"
                )

            return job
        except Exception as exc:
            raise_error(exc)
    
    
    @staticmethod
    async def create(
        payload: JobCategoryCreate,
        db: Session
    ):
        try:
            await JobCategoryService.find_by_name(payload.name)
            job = JobCategory(
                name=payload.name.capitalize().strip()
            )

            db.add(job)
            db.commit()
            db.refresh(job)
            return job
        except Exception as exc:
            raise_error(exc)