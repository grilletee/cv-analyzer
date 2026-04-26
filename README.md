# CV Analyzer API

API REST que analiza CVs usando IA (Google Gemini) y devuelve feedback estructurado en JSON.

🚀 **Demo en producción:** https://cv-analyzer-37jx.onrender.com/docs

> El primer request puede tardar ~50 segundos si la instancia está inactiva (plan gratuito de Render).

## ¿Qué hace?

- Analiza un CV en texto plano y devuelve puntuación, fortalezas, debilidades y sugerencias
- Acepta CVs en formato PDF
- Compara un CV contra una oferta de trabajo y calcula el nivel de match
- Devuelve siempre JSON estructurado y validado
- Todos los endpoints están protegidos por autenticación con API Key

## Stack

- **Python 3.13** + **FastAPI** — API REST con validación automática
- **Google Gemini 2.5 Flash** — Modelo de IA para el análisis
- **Pydantic v2** — Validación de schemas de entrada y salida
- **pypdf** — Extracción de texto de archivos PDF
- **pytest** — Tests con mocks, sin consumir API en cada ejecución
- **Render** — Despliegue con CI/CD automático en cada push

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/cv/analyze` | Analiza un CV en texto plano |
| `POST` | `/api/v1/cv/analyze-pdf` | Analiza un CV en formato PDF |
| `POST` | `/api/v1/cv/match` | Compara CV contra oferta de trabajo |
| `GET` | `/api/v1/health` | Healthcheck |

## Autenticación

Todos los endpoints requieren el header `X-API-Key`:

```bash
curl -X POST https://cv-analyzer-37jx.onrender.com/api/v1/cv/analyze \
  -H "X-API-Key: tu_api_key" \
  -H "Content-Type: application/json" \
  -d '{"cv_text": "Tu CV aquí..."}'
```

## Ejemplo de respuesta

```json
{
  "score": 75,
  "summary": "Desarrollador frontend con experiencia en React...",
  "strengths": ["React", "JavaScript"],
  "weaknesses": ["Testing", "Backend"],
  "suggestions": ["Aprender TypeScript"],
  "keywords_missing": ["TypeScript", "Jest"],
  "estimated_level": "mid"
}
```

## Instalación local

```bash
git clone https://github.com/grilletee/cv-analyzer.git
cd cv-analyzer
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crea un `.env` con tus variables:

```
GEMINI_API_KEY=tu_key_de_google_ai_studio
API_KEY=tu_clave_secreta
APP_ENV=development
```

Arranca la API:

```bash
uvicorn app.main:app --reload
```

Documentación interactiva en `http://127.0.0.1:8000/docs`

## Tests

```bash
pytest tests/ -v
```

## Estructura

```
cv-analyzer/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuración con pydantic-settings
│   ├── dependencies.py      # Inyección del cliente Gemini y autenticación
│   ├── routers/
│   │   └── cv.py            # Endpoints HTTP
│   ├── schemas/
│   │   └── cv.py            # Modelos Pydantic
│   └── services/
│       ├── cv_analyzer.py   # Lógica de análisis con Gemini
│       └── pdf_extractor.py # Extracción de texto de PDFs
└── tests/
    └── test_cv.py           # Tests con mocks
```