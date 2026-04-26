from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from google import genai
from app.dependencies import get_gemini_client, verify_api_key
from app.schemas.cv import CVAnalysisRequest, CVAnalysisResponse
from app.services.cv_analyzer import analyze_cv
from app.services.pdf_extractor import extract_text_from_pdf

router = APIRouter(prefix="/api/v1/cv", tags=["CV"])


@router.post("/analyze", response_model=CVAnalysisResponse)
def analyze(
    request: CVAnalysisRequest,
    client: genai.Client = Depends(get_gemini_client),
    _: str = Depends(verify_api_key)
):
    try:
        return analyze_cv(request, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-pdf", response_model=CVAnalysisResponse)
async def analyze_pdf(
    file: UploadFile = File(...),
    job_description: str | None = Form(None),
    client: genai.Client = Depends(get_gemini_client),
    _: str = Depends(verify_api_key)
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")

    try:
        file_bytes = await file.read()
        cv_text = extract_text_from_pdf(file_bytes)
        request = CVAnalysisRequest(cv_text=cv_text, job_description=job_description)
        return analyze_cv(request, client)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/match", response_model=CVAnalysisResponse)
def match(
    request: CVAnalysisRequest,
    client: genai.Client = Depends(get_gemini_client),
    _: str = Depends(verify_api_key)
):
    if not request.job_description:
        raise HTTPException(status_code=400, detail="job_description es obligatorio para /match")
    try:
        return analyze_cv(request, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))