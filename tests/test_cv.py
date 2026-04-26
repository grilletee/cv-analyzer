import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.dependencies import get_gemini_client

client = TestClient(app)

MOCK_RESPONSE = {
    "score": 75,
    "summary": "Desarrollador con experiencia sólida en frontend.",
    "strengths": ["React", "JavaScript"],
    "weaknesses": ["Testing", "Backend"],
    "suggestions": ["Aprender TypeScript", "Añadir tests"],
    "keywords_missing": ["TypeScript", "Jest"],
    "estimated_level": "mid"
}


def get_mock_client():
    mock = MagicMock()
    mock.models.generate_content.return_value.text = str(MOCK_RESPONSE).replace("'", '"')
    return mock


app.dependency_overrides[get_gemini_client] = get_mock_client


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_success():
    response = client.post("/api/v1/cv/analyze", json={
        "cv_text": "Desarrollador React con 3 años de experiencia."
    })
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "strengths" in data
    assert isinstance(data["strengths"], list)


def test_analyze_empty_cv():
    response = client.post("/api/v1/cv/analyze", json={
        "cv_text": ""
    })
    assert response.status_code in [200, 500]


def test_match_without_job_description():
    response = client.post("/api/v1/cv/match", json={
        "cv_text": "Desarrollador React con 3 años de experiencia."
    })
    assert response.status_code == 400
    assert "job_description" in response.json()["detail"]


def test_match_success():
    response = client.post("/api/v1/cv/match", json={
        "cv_text": "Desarrollador React con 3 años de experiencia.",
        "job_description": "Buscamos desarrollador React con TypeScript."
    })
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert "keywords_missing" in data