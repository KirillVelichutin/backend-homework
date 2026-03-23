from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api import common_router
from core.exceptions import AppException

app = FastAPI()


@app.exception_handler(AppException)
def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
            }
        },
    )


app.include_router(common_router)
