import logging
import sys
from fastapi import FastAPI
from src.core.container import Container
from src.api.routes import router as parser_router
from src.db.models import Base

# логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    container = Container()

    db_engine = container.db_engine()
    Base.metadata.create_all(bind=db_engine)

    app = FastAPI(
        title="Higher School of Parsing",
        description="Система для сбора, хранения и визуализации данных с различных веб-ресурсов",
        version="1.0.0",
    )

    app.container = container
    
    app.include_router(parser_router, prefix="/api/v1", tags=["Scrapers"])

    @app.get("/")
    async def is_alive():
        logger.info("is_alive requested")
        return {
            "status": "ok",
            "message": "System is running",
            "container_active": True
        }
    
    return app

app = create_app()