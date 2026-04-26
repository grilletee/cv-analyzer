from fastapi import FastAPI
from app.routers import cv

app = FastAPI(
    title="CV Analyzer API",
    description="API REST para analizar CVs usando IA",
    version="1.0.0"
)

app.include_router(cv.router)


@app.get("/api/v1/health", tags=["Health"])
def health():
    return {"status": "ok"}