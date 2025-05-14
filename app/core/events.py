from typing import Callable

import joblib
from fastapi import FastAPI

from app.db.base import Base, engine


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        Base.metadata.create_all(bind=engine)

    return start_app
