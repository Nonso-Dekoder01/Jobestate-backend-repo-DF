from pydantic import ValidationError

class PydanticValidationError:
    @staticmethod
    def parse_error(exc: ValidationError):
        errors = exc.errors()
        parsed_errors = []

        for error in errors:
            parsed_errors.append(
                {
                    "error_type": error["type"],
                    "locations": {",".join(error["loc"])},
                    "message": error["msg"],
                    "input": error["input"],
                    # "url": error.get("url",None)
                }
            )
        return parsed_errors