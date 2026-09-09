import sys
from pathlib import Path

# Ensure backend directory is in python search path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from investigations.gemini_explanation import generate_gemini_explanation

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from investigations.engine import (
    investigate,
    generate_causal_hypotheses,
)
from investigations.competing_events import detect_competing_events


# ---------------------------------------------------------
# App
# ---------------------------------------------------------

app = FastAPI(
    title="Echo",
    description="Deployment intelligence and root-cause investigation engine",
    version="0.1.0",
)


import os

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

origins_env = os.getenv("ALLOWED_ORIGINS")
if origins_env:
    allowed_origins = [o.strip() for o in origins_env.split(",") if o.strip()]
else:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "echo-backend",
    }


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Echo API</title>
        </head>

        <body
            style="
                font-family: Arial, sans-serif;
                padding: 40px;
                background: #0b0d10;
                color: white;
            "
        >
            <h1>🔊 Echo</h1>

            <p>
                Deployment intelligence backend is running.
            </p>

            <p>
                API:
                <strong>localhost:8000</strong>
            </p>

            <p>
                Health:
                <a
                    href="/health"
                    style="color: #66b3ff;"
                >
                    /health
                </a>
            </p>

            <p>
                API documentation:
                <a
                    href="/docs"
                    style="color: #66b3ff;"
                >
                    /docs
                </a>
            </p>
        </body>
    </html>
    """


# ---------------------------------------------------------
# Investigate deployment
# ---------------------------------------------------------

@app.get("/api/investigate/{deployment_id}")
def investigate_deployment(deployment_id: str):
    """
    Run the complete Echo investigation for a deployment.

    Example:
        /api/investigate/DEP-4821
    """

    try:
        result = investigate(deployment_id)

        if result.get("status") == "NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail=result,
            )

        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "ERROR",
                "message": str(exc),
            },
        )


# ---------------------------------------------------------
# Causal hypotheses
# ---------------------------------------------------------

@app.get("/api/hypothesis/{deployment_id}")
def deployment_hypothesis(deployment_id: str):
    """
    Generate causal hypotheses for a deployment.

    Example:
        /api/hypothesis/DEP-4821
    """

    try:
        result = generate_causal_hypotheses(deployment_id)

        if result.get("status") == "NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail=result,
            )

        return result

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "ERROR",
                "message": str(exc),
            },
        )


# ---------------------------------------------------------
# Competing events
# ---------------------------------------------------------

@app.get("/api/events/{deployment_id}")
def competing_events(deployment_id: str):
    """
    Find external or competing events around a deployment.

    Example:
        /api/events/DEP-4822
    """

    try:
        result = detect_competing_events(deployment_id)

        return {
            "deployment_id": deployment_id,
            "events": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "ERROR",
                "message": str(exc),
            },
        )


# ---------------------------------------------------------
# Combined investigation endpoint
# ---------------------------------------------------------

@app.get("/api/investigation/{deployment_id}")
def complete_investigation(deployment_id: str):
    """
    Combined endpoint for the Echo frontend.

    Returns:
        - deployment
        - system impact
        - product impact
        - business impact
        - hypotheses
        - competing events
    """

    try:
        investigation = investigate(deployment_id)

        if investigation.get("status") == "NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail=investigation,
            )

        hypotheses = generate_causal_hypotheses(deployment_id)

        events = detect_competing_events(deployment_id)

        return {
            **investigation,
            "hypotheses": hypotheses.get(
                "hypotheses",
                [],
            ),
            "competing_events": events,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "ERROR",
                "message": str(exc),
            },
        )


# ---------------------------------------------------------
# Startup message
# ---------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    print("")
    print("🔊 Echo backend started")
    print("   API:    http://localhost:8000")
    print("   Health: http://localhost:8000/health")
    print("   Docs:   http://localhost:8000/docs")
    print("")

@app.get("/api/explanation/{deployment_id}")
def get_gemini_explanation(deployment_id: str):
    try:
        investigation = generate_causal_hypotheses(deployment_id)

        explanation = generate_gemini_explanation(
            investigation,
            investigation
        )

        return {
            "status": "SUCCESS",
            "deployment_id": deployment_id,
            "explanation": explanation,
        }

    except Exception as exc:
        return {
            "status": "ERROR",
            "deployment_id": deployment_id,
            "message": str(exc),
        }