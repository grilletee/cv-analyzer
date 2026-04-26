import json
from google import genai
from app.schemas.cv import CVAnalysisRequest, CVAnalysisResponse


def analyze_cv(request: CVAnalysisRequest, client: genai.Client) -> CVAnalysisResponse:
    prompt = f"""
    Analiza el siguiente CV y devuelve ÚNICAMENTE un JSON válido con esta estructura exacta, sin texto adicional, sin markdown, sin bloques de código:
    {{
        "score": número del 0 al 100,
        "summary": "resumen breve del perfil",
        "strengths": ["fortaleza 1", "fortaleza 2"],
        "weaknesses": ["debilidad 1", "debilidad 2"],
        "suggestions": ["sugerencia 1", "sugerencia 2"],
        "keywords_missing": ["keyword 1", "keyword 2"],
        "estimated_level": "junior | mid | senior"
    }}

    CV:
    {request.cv_text}

    {"Descripción del puesto: " + request.job_description if request.job_description else ""}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()
    data = json.loads(raw)
    return CVAnalysisResponse(**data)