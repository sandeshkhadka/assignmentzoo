from sqlalchemy.orm import Session

from app.db.models import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Project)
        .order_by(Project.upvotes.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def search_projects_by_name(db: Session, name: str):
    return db.query(Project).filter(Project.name.ilike(f"%{name}%")).all()


def search_projects_by_author(db: Session, author_name: str):
    return db.query(Project).filter(Project.author_name.ilike(f"%{author_name}%")).all()


def create_project(db: Session, project: ProjectCreate):
    db_project = Project(
        name=project.name,
        github_url=project.github_url,
        author_name=project.author_name,
        module_name=project.module_name,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        return None

    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if not db_project:
        return False

    db.delete(db_project)
    db.commit()
    return True
