from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_jwt_auth2.exceptions import AuthJWTException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from src.api.v1.routes.router import router as router_v1
from src.core.config import settings
from src.core.logger import logger


@asynccontextmanager
async def lifespan(app_: FastAPI):
    logger.info("Starting FastAPI app")
    yield
    logger.info("Shutting down FastAPI app")


app = FastAPI(
    lifespan=lifespan,
    version=settings.PROJECT_VERSION,
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
)


app.include_router(router_v1)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "details": exc.message},
    )


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
