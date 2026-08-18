from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import Base, engine
from .api.routes import auth, books

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Store API",
    description="Backend API for the Book Store - manage books with multiple images, login, and signup",
    version="1.0.0",
    # Disable auto-generated API docs (/docs, /redoc, /openapi.json)
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(books.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Welcome to Book Store API",
        "health": "/api/health",
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok"}