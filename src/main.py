import logging
import sys
from fastapi import FastAPI
from src.core.container import Container

# логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(
        title="Higher School of Parsing",
        description="Система для сбора, хранения и визуализации данных с различных веб-ресурсов",
        version="1.0.0",
    )

    app.container = container

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