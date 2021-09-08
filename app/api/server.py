from fastapi import FastAPI
from app.core.tasks import (create_start_app_handler, create_stop_app_handler)


def get_application() -> FastAPI:
    """Create fastapi application with all routes and handlers"""
    app = FastAPI()

    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))

    return app


application = get_application()
