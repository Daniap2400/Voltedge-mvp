import logging
import time

from fastapi import FastAPI, Request

from app.api.routes import api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("voltedge.api")

app = FastAPI(
    title="VoltEdge API",
    description="Technical MVP API for Smart EV Charging Infrastructure",
    version="0.1.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    logger.info(
        "API request completed method=%s path=%s status_code=%s duration_ms=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response


@app.get("/")
def read_root():
    return {
        "service": "voltedge-api",
        "status": "running",
        "stage": "api-foundation",
        "docs": "/docs",
        "api_v1": "/api/v1",
    }


@app.get("/health")
def root_health_check():
    return {
        "status": "healthy",
        "service": "voltedge-api",
    }


app.include_router(api_router)