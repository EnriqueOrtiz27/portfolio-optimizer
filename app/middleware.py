import traceback

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from app.errors import ErrorResponse, ErrorCode


async def validation_exception_handler(_: Request, exc: RequestValidationError):
    error_messages = []

    for error in exc.errors():
        loc = ".".join(
            str(x) for x in error["loc"]
        )  # Get the location of the error (e.g., field name)
        msg = error["msg"]  # The error message
        error_messages.append(f"Field '{loc}': {msg}")

    message = ". ".join(error_messages)
    error = ErrorResponse(code="unprocessable_entity", message=message)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=error.model_dump()
    )


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as e:
        traceback.print_exc()
        response = ErrorResponse(code=ErrorCode.bad_request, message=e.detail)
        return JSONResponse(
            content=response.model_dump(),
            status_code=e.status_code
        )
    except ValueError as e:
        traceback.print_exc()
        message = "Please upload a valid CSV"
        response = ErrorResponse(code=ErrorCode.bad_request, message=message)
        return JSONResponse(
            content=response.model_dump(), status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        traceback.print_exc()
        response = ErrorResponse(
            code=ErrorCode.unknown_error, message="Something went wrong on our end and we will try to fix it."
        )
        return JSONResponse(
            content=response.model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
