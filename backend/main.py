import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.logger import logger
from backend.db.connector import engine
from backend.db.models import Base
from backend.routers.v1 import (
    dashboards,
    sleep_goals,
    sleep_logs,
    sleep_reports,
    users,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="SleepMate API",
        description="API для трекера сна с AI-отчётами",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(
        sleep_logs.router, prefix="/api/v1/sleep", tags=["Sleep Logs"]
    )
    app.include_router(
        sleep_goals.router, prefix="/api/v1/goals", tags=["Sleep goals"]
    )
    app.include_router(
        dashboards.router, prefix="/api/v1/goals", tags=["Analytics"]
    )
    app.include_router(
        sleep_reports.router, prefix="/api/v1/reports", tags=["Sleep Reports"]
    )

    @app.on_event("startup")
    async def on_startup() -> None:
        logger.info("Приложение запущено")

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
