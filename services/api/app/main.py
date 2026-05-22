from fastapi import FastAPI

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
        "stage": "foundation"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }