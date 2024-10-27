from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import RedirectResponse

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


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url="/docs")
