from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logger import logger

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    
    logger.warning(
            f"{request.method} {request.url.path} -> {exc.status_code}: {exc.detail}"
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "detail": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    
    logger.warning(
            f"Validation error on {request.method} {request.url.path}: {exc.errors()}"
         )

    return JSONResponse(
        status_code=422,
        content={"success": False, "detail": exc.errors()},
    )


async def global_exception_handler(request: Request, exc: Exception):

    logger.exception(f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}"
                    )

    return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "detail":"Internal server error",
                },
            )
