from api.routes.api import router as api_router
from core.config import API_PREFIX, DEBUG, FRONTEND_PREFIX, PROJECT_NAME, VERSION
from core.events import create_start_app_handler
from fastapi.staticfiles import StaticFiles
from frontend.routes import frontend_router

from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.mount("/static", StaticFiles(directory="app/static"), name="static")
    application.include_router(api_router, prefix=API_PREFIX)
    application.include_router(frontend_router, prefix=FRONTEND_PREFIX)
    application.add_event_handler(
        "startup",
        create_start_app_handler(application),
    )
    return application


app = get_application()
