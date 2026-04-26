from pydantic import BaseModel


class CVAnalysisRequest(BaseModel):
    cv_text: str
    job_description: str | None = None


class CVAnalysisResponse(BaseModel):
    score: int
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
    keywords_missing: list[str]
    estimated_level: str