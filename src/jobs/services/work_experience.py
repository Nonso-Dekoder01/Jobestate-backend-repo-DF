from uuid import UUID
from fastapi import HTTPException

from errors.error import raise_error
from src.jobs.models import WorkExperience
from src.jobs.schemas import AddWorkExperience


class WorkExperienceService:
    @staticmethod
    async def add_work_experience(
        payload: AddWorkExperience,
        user_id: UUID,
        db # Type Session
    ):
        try:
            work_experience = WorkExperience(
                **payload.model_dump(),
                user_id=user_id
            )

            db.add(work_experience)
            db.commit()
            db.refresh(work_experience)

            return work_experience
        except Exception as exc:
            raise_error(exc)

    
    @staticmethod
    async def get_all_user_work_experience(
        user_id: UUID,
        db # Type Session
    ):
        try:
            return (
                db
                .query(WorkExperience)
                .filter_by(user_id=user_id)
                .all()
            )
        except Exception as exc:
            raise_error(exc)

    
    @staticmethod
    async def remove_work_experience(
        work_experience_id: UUID,
        user_id: UUID,
        db # Type Session
    ):
        try:
            work_experience = db.query(WorkExperience).filter_by(
                id_=work_experience_id,
                user_id=user_id
            )

            if not work_experience:
                raise HTTPException(
                    404,
                    "Work Experience not found."
                )
            
            db.delete(work_experience)
            db.commit()
        except Exception as exc:
            raise_error(exc)