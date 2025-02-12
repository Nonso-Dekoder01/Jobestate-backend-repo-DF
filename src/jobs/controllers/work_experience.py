from uuid import UUID

from fastapi import Depends

from config.db import get_db
from errors import parse_error

from response import Response

from src.jobs.services import WorkExperienceService
from src.auth.services import UserService
from src.jobs.schemas import AddWorkExperience


class WorkExperienceController:

    @staticmethod
    async def get_all_user_work_experience(
        db = Depends(get_db),
        token = Depends(UserService.get_current_user)
    ):
        try:
            previous_jobs = (
                await WorkExperienceService
                .get_all_user_work_experience(token.user.id_, db)
            )

            return Response(
                previous_jobs
            )
        except Exception as exc:
            return parse_error(exc)


    async def remove_work_experience(
        work_experience_id: UUID,
        token = Depends(UserService.get_current_user),
        db = Depends(get_db)
    ):
        try:
            (
                await WorkExperienceService
                .remove_work_experience(
                    work_experience_id,
                    token.user.id_,
                    db
                )
            )

            return Response(
                message="Removed successfully"
            )
        except Exception as exc:
            return parse_error(exc)
        

    async def add_work_experience(
        payload: AddWorkExperience,
        token = Depends(UserService.get_current_user),
        db = Depends(get_db)
    ):
        try:
            work_experience = (
                await WorkExperienceService
                .add_work_experience(
                    payload,
                    token.user.id_,
                    db
                )
            )

            return Response(
                work_experience
            )
        except Exception as exc:
            return parse_error(exc)