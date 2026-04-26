import json
import re
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

    # Elimina bloques markdown si Gemini los añade igualmente
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini devolvió una respuesta no parseable como JSON: {e}\nRespuesta raw: {raw}")

    required_keys = {"score", "summary", "strengths", "weaknesses", "suggestions", "keywords_missing", "estimated_level"}
    missing = required_keys - data.keys()
    if missing:
        raise ValueError(f"La respuesta de Gemini omitió campos obligatorios: {missing}")

    return CVAnalysisResponse(**data)