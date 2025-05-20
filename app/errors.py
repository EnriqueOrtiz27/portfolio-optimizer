from enum import Enum, unique

from pydantic import BaseModel


@unique
class ErrorCode(str, Enum):
    unknown_error = "unknown_error"
    bad_request = "bad_request"
    unprocessable_entity = "unprocessable_entity"


class ErrorResponse(BaseModel):
    code: ErrorCode
    message: str
