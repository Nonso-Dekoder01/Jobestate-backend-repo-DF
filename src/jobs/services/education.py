from fastapi import HTTPException
from errors.error import raise_error
from src.jobs.models import Education


class EducationService:
    @staticmethod
    async def add_education(
        payload,
        user_id,
        db
    ):
        """
            payload (AddEducation): education body

            user_id (UUID): user id

            db (Session): database Session objectt  
        """
        try:
            education = Education(
                **payload.model_dump(),
                user_id=user_id
            )

            db.add(education)
            db.commit()
            db.refresh(education)

            return education
        except Exception as exc:
            raise_error(exc)


    @staticmethod
    async def get_all_user_education(
        user_id,
        db
    ):
        """
        user_id (UUID): user id

        db (Session): database Session objectt
        """
        try:
            return (
                db
                .query(Education)
                .filter(user_id=user_id)
                .all()
            )
        except Exception as exc:
            raise_error(exc)

    
    @staticmethod
    async def remove_education(
        education_id,
        user_id,
        db
    ):
        """
            education_id (UUID): education id

            user_id (UUID): user id

            db (Session): database Session objectt  
        """
        try:
            education = (
                db.query(Education)
                .filter(id_=education_id,user_id=user_id)
                .first()
            )
            if not education:
                raise HTTPException(
                    404,
                    f"Education {education_id} not found"
                )

            db.delete(education)
            db.commit()
        except Exception as exc:
            raise_error(exc)