from app.crud.project import get_projects
from app.db.base import get_db
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
templates = Jinja2Templates(directory="app/templates")

frontend_router = APIRouter()

@frontend_router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    projects = get_projects(db)
    # projects = 
    return templates.TemplateResponse("index.html", {"request": request, "projects": projects})

@frontend_router.get("/submit", response_class=HTMLResponse)
async def submit_page(request: Request):
    return templates.TemplateResponse("submit.html", {"request": request})

