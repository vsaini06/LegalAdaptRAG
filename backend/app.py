import logging
import logging.config
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings, Settings

# Logging

def configure_logging(settings: Settings) -> None:
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": settings.log_level.upper(),
            "handlers": ["console"],
        },
    })

# Lifespan

def build_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        logger = logging.getLogger(__name__)
        logger.info("Starting LegalAdaptRAG")
        logger.info("Environment : %s", settings.environment)
        logger.info("Log level   : %s", settings.log_level.upper())
        yield
        logger.info("LegalAdaptRAG shut down cleanly")

    return lifespan

# Middleware

def register_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

# Routes

def register_routes(app: FastAPI) -> None:
    @app.get("/health", tags=["ops"])
    async def health():
        return {"status": "ok", "version": app.version}

# App factory

def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(
        title="LegalAdaptRAG",
        description="Intent-aware adaptive retrieval for legal document understanding",
        version="0.1.0",
        lifespan=build_lifespan(settings),
        docs_url="/docs" if settings.environment == "development" else None,
        redoc_url=None,
    )

    register_middleware(app, settings)
    register_routes(app)

    return app


app = create_app()