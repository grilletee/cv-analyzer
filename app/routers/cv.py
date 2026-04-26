from fastapi import APIRouter, Depends, HTTPException
from google import genai
from app.dependencies import get_gemini_client
from app.schemas.cv import CVAnalysisRequest, CVAnalysisResponse
from app.services.cv_analyzer import analyze_cv

router = APIRouter(prefix="/api/v1/cv", tags=["CV"])


@router.post("/analyze", response_model=CVAnalysisResponse)
def analyze(
    request: CVAnalysisRequest,
    client: genai.Client = Depends(get_gemini_client)
):
    try:
        return analyze_cv(request, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/match", response_model=CVAnalysisResponse)
def match(
    request: CVAnalysisRequest,
    client: genai.Client = Depends(get_gemini_client)
):
    if not request.job_description:
        raise HTTPException(status_code=400, detail="job_description es obligatorio para /match")
    try:
        return analyze_cv(request, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))