from fastapi import FastAPI

from app.api.routes import api_router

app = FastAPI(
    title="VoltEdge API",
    description="Technical MVP API for Smart EV Charging Infrastructure",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "service": "voltedge-api",
        "status": "running",
        "stage": "api-foundation",
        "docs": "/docs",
        "api_v1": "/api/v1"
    }


@app.get("/health")
def root_health_check():
    return {
        "status": "healthy",
        "service": "voltedge-api"
    }


app.include_router(api_router)