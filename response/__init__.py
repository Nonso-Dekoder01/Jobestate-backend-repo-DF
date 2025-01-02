from typing import Any, List, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class Response(JSONResponse):
    def __init__(self,
        data: Any = {},
        errors: Optional[List[dict]] = None,
        message: str = "Successful",
        links: List = [],
        status_code: int = 200
        ) -> None:
        
        self.content = {
        "message":message,
        "data"  : jsonable_encoder(data),
        "errors":jsonable_encoder(errors), 
        "links":links
        }

        super().__init__(self.content, status_code)