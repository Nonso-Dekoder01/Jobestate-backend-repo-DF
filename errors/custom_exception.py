import http
from typing import  Dict, List
from fastapi import HTTPException


class JobStateException(HTTPException):
    def __init__(
            self, 
            status_code: int,
            errors: List[Dict[str, str]],
            links: List = [],
            detail: str = None, 
            headers: Dict[str, str] | None = None
            ) -> None:
        super().__init__(status_code, detail, headers)
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.detail = detail
        self.errors = errors
        self.errors = errors
        self.links = links

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail} : {self.errors}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"
    

    def parse_external_error(
            response_code: str,
            message: str
    ):
        """
            Forms an error that is resulted
            from an issue with an external API
        """
        raise JobStateException(
            500,
            [{response_code:message}],
            detail="Please contact the backend engineer to address the error in question"
        )    