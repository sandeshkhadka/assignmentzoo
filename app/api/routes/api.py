from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.paginator import pagenation
from app.crud.project import (
    create_project,
    delete_project,
    get_project,
    get_projects,
    search_projects_by_author,
    search_projects_by_name,
    update_project,
)
from app.db.base import get_db
from app.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()


@router.get("/projects", response_model=list[Project])
async def fetch_projects(page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    projects = get_projects(db)
    total = len(projects)
    result = pagenation(page, size, total, projects)
    return result["listings"]


@router.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
async def add_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, project)


@router.get("/projects/{project_id}", response_model=Project)
async def get_project_by_id(project_id: int, db: Session = Depends(get_db)):
    db_project = get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/projects/{project_id}", response_model=Project)
async def update_project_by_id(
    project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)
):
    db_project = update_project(db, project_id, project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_by_id(project_id: int, db: Session = Depends(get_db)):
    success = delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return None


@router.get("/projects/search/name/{name}", response_model=list[Project])
async def search_projects_name(name: str, db: Session = Depends(get_db)):
    projects = search_projects_by_name(db, name)
    return projects


@router.get("/projects/search/author/{author_name}", response_model=list[Project])
async def search_projects_author(author_name: str, db: Session = Depends(get_db)):
    projects = search_projects_by_author(db, author_name)
    return projects
