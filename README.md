# CV Analyzer API

API REST que analiza CVs usando IA (Google Gemini) y devuelve feedback estructurado en JSON.

## ¿Qué hace?

- Analiza un CV en texto plano y devuelve puntuación, fortalezas, debilidades y sugerencias
- Compara un CV contra una oferta de trabajo y calcula el nivel de match
- Devuelve siempre JSON estructurado y validado

## Stack

- **Python 3.13** + **FastAPI** — API REST con validación automática
- **Google Gemini 2.5 Flash** — Modelo de IA para el análisis
- **Pydantic v2** — Validación de schemas de entrada y salida
- **pytest** — Tests con mocks, sin consumir API en cada ejecución

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/v1/cv/analyze` | Analiza un CV |
| `POST` | `/api/v1/cv/match` | Compara CV contra oferta de trabajo |
| `GET` | `/api/v1/health` | Healthcheck |

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

Crea un `.env` con tu API key:

```
GEMINI_API_KEY=tu_key_aqui
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
│   ├── main.py          # FastAPI app
│   ├── config.py        # Configuración con pydantic-settings
│   ├── dependencies.py  # Inyección del cliente Gemini
│   ├── routers/         # Endpoints HTTP
│   ├── schemas/         # Modelos Pydantic
│   └── services/        # Lógica de negocio
└── tests/               # Tests con pytest
```