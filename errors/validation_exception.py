from fastapi.exceptions import RequestValidationError

from response import Response

def validation_exception_handler(exc:RequestValidationError):
    errors = []
    errs = exc.errors()
    for error in errs:
        if error['type'] == 'missing' and len(error['loc']) > 1:
            if error['loc'][0] == 'header':
                return Response(
                status_code=401,
                errors=[{
                    error['loc'][0]:f'{error["loc"][1]} must not be empty'
                }],
                message=f"Unauthorized"
            )

            elif error['loc'][0] == 'body':
                if error['loc'][0]:
                    column = error['loc'][1] if len(error['loc']) < 3 else error['loc'][2]
                    errors.append({error['loc'][1]:f"{column} must not be empty"})
        elif error["loc"][0] == "query":
            errors.append({error["type"]:error["msg"]})
    if errors:
        return Response(
            status_code=400,
            errors=errors,
            message="Bad request"
        )
    elif errs[0]['type'] == 'missing':
        return Response(
        status_code=400,
        errors=[{
            errs[0]["loc"][0]:f'{errs[0]["loc"][0]} must not be empty'
        }],
        message="Bad request"
    )
    elif errs[0]['type'] == 'model_attributes_type':
        return Response(
            status_code=400,
            message="Bad request",
            errors=[{
                errs[0]['loc'][0]: errs[0]['msg']
            }]
        )
    elif errs[0]['type'] == "string_too_long":
        return Response(
            status_code=400,
            data=None,
            message="Bad request",
            errors=[{
                errs[0]['loc'][0]: f"{errs[0]['loc'][1]} {errs[0]['msg']}"
            }]
        )
    elif errs[0].get("loc")[0] == "body":
        return Response(
            status_code=400,
            message="Bad request",
            errors=[{
                errs[0]['loc'][1]:errs[0]['msg'] 
            }]
        )
    else:
        return Response(
            errors=[{"server":'An error occured'}],
            message='Unable to proceed',
            status_code=500
        )