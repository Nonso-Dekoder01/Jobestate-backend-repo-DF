import http
from requests import ConnectionError
from fastapi import HTTPException
# from botocore.exceptions import EndpointConnectionError
from pydantic import ValidationError
from json.decoder import JSONDecodeError
from jwt.exceptions import ExpiredSignatureError
from .pydantic_validation import PydanticValidationError
from .custom_exception import JobStateException

from response import Response

def raise_error(exc):
    if type(exc) is JobStateException:
        raise exc
    if type(exc) is Exception:
        raise JobStateException(
            500,
            [{"error":str(exc)}],
            detail="Internal server error"
        )
    if type(exc) is ValidationError:
        raise JobStateException(
            400,
            PydanticValidationError.parse_error(exc),
            detail="Bad request"
        )
    if type(exc) is JSONDecodeError:
        raise JobStateException(
            503,
            [{"request": "Invalid JSON format"}],
            detail="This is likely due to the backend server not being able to parse the JSON data sent by the client. Please contact the engineer in charge of the API for further assistance."
        )
    elif type(exc) is ValueError:
        raise JobStateException(400,[{"request":exc.args}])
    elif type(exc) is ConnectionError:
        raise JobStateException(408, [{"network":"Please check your network and try again."}],detail="Network connection error")
    if type(exc) is HTTPException:
        raise JobStateException(
            exc.status_code,
            detail=http.HTTPStatus(exc.status_code).phrase,
            errors=[{
                exc.status_code: exc.detail
            }]
        )
    # if type(exc) is EndpointConnectionError:
    #     raise JobStateException(
    #         408,
    #         {"network":"Please check your network and try again"},
    #         detail="Network timeout"
    #     )
    else:
        raise JobStateException(
            500,
            [{"server":str(exc)}],
            detail="Internal server error"
        )
    # elif type(exc) is ExpiredSignatureError:
    #     raise HTTPException(400, ["Bad request","Your session has expired"])
    # else:
    #     raise HTTPException(500, str(exc))
    
def parse_error(exc):
    if type(exc) is ExpiredSignatureError:
        return Response(
            errors=[{"token":"Session expired"}],
            message="Please go back to login",
            status="failed",
            status_code=400
        )
    if type(exc) is JobStateException:
        print(exc)
        return Response(
            errors=exc.errors,
            message=exc.detail,
            status_code=exc.status_code,
            links=exc.links
        )
    if type(exc) is HTTPException:
        if type(exc.detail) is list:
            errors = exc.detail
            return Response(
                errors[3] if len(errors) > 3 else None, 
                errors=[errors[1]],
                message=errors[0],
                status_code=exc.status_code,
                links=errors[2] if len(errors) >= 3 else []
            )
        if exc.status_code == 408:
            return Response(
                errors=[{"network":"Request Timeout"}],
                message="Please check your network and try again",
                status_code=408
            )
        return Response(
            None,
            errors=[{exc.status_code:exc.detail}],
            message="an error occured",
            status_code=exc.status_code
        )
    if type(exc) is ValidationError:
        return Response(
            None,
            PydanticValidationError.parse_error(exc),
            message="An error occurred",
            status_code=400
        )
    return Response(
        None,
        message="An error occurred",
        status_code=500,
        errors=exc.detail if type(exc) is HTTPException else str(exc)
    )