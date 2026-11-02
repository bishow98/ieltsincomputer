import logging
import re
import os
# pyrefly: ignore [missing-import]
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine
from app import models
from app.routers import auth, tests, sessions, submissions, payments, dashboard, admin, subscription_requests, contact, mock_test, enterprise
from app.routers.dashboard import vocab_router

# Create all tables
models.Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="IELTSPrep API",
    description="Full-featured IELTS Practice Platform with AI scoring",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

def parse_origins(raw: str) -> list[str]:
    return [o.strip() for o in re.split(r"[, ]+", raw) if o.strip()]

origins = [settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"]
if settings.CORS_ORIGINS:
    origins.extend(parse_origins(settings.CORS_ORIGINS))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (audio, images, uploads)
os.makedirs("static/audio", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/uploads/subscriptions", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(tests.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(submissions.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(vocab_router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(subscription_requests.router, prefix="/api/v1")
app.include_router(contact.router, prefix="/api/v1")
app.include_router(mock_test.router, prefix="/api/v1")
app.include_router(enterprise.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/seed-massive")
def seed_massive_endpoint():
    import traceback
    try:
        with open("seed_massive.py", "r") as f:
            code = f.read()
        exec(code, globals())
        seed_massive()
        return {"status": "seeded_full_content"}
    except Exception as e:
        return {"status": "error", "traceback": traceback.format_exc()}


@app.get("/test-import")
def test_import():
    import traceback
    try:
        with open("/home/bishow/.gemini/antigravity-ide/brain/ce0ef029-f0cb-42db-9175-b77f347ced12/scratch/build_seeder.py", "r") as f:
            code = f.read()
        exec(code, globals())
        return {"status": "built_seeder"}
    except Exception as e:
        return {"error": traceback.format_exc()}


