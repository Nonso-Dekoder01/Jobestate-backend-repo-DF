from uuid import UUID

from fastapi import Depends

from config.db import get_db
from errors import parse_error

from response import Response

from src.jobs.services import EducationService
from src.auth.services import UserService
from src.jobs.schemas import AddEducation


class EducationController:

    @staticmethod
    async def get_all_user_education(
        db = Depends(get_db),
        token = Depends(UserService.get_current_user)
    ):
        try:
            educations = (
                await EducationService
                .get_all_user_education(token.user.id_, db)
            )

            return Response(
                educations
            )
        except Exception as exc:
            return parse_error(exc)


    async def remove_education(
        education_id: UUID,
        token = Depends(UserService.get_current_user),
        db = Depends(get_db)
    ):
        try:
            (
                await EducationService
                .remove_education(
                    education_id,
                    token.user.id_,
                    db
                )
            )

            return Response(
                message="Removed successfully"
            )
        except Exception as exc:
            return parse_error(exc)
        

    async def add_education(
        payload: AddEducation,
        token = Depends(UserService.get_current_user),
        db = Depends(get_db)
    ):
        try:
            education = (
                await EducationService
                .add_education(
                    payload,
                    token.user.id_,
                    db
                )
            )

            return Response(
                education
            )
        except Exception as exc:
            return parse_error(exc)