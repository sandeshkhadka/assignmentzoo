import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.crud.project import (
    create_project,
    delete_project,
    get_project,
    get_projects,
    search_projects_by_author,
    search_projects_by_name,
    update_project,
)
from app.db.models import Base, Project
from app.schemas.project import ProjectCreate, ProjectUpdate


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_project(db_session):
    """Create a sample project for testing."""
    project = Project(
        name="Test Project",
        github_url="https://github.com/user/test-project",
        author_name="Test User",
        module_name="test_module",
        upvotes=5,
    )
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


def test_get_project(db_session, sample_project):
    """Test retrieving a project by ID."""
    project = get_project(db_session, sample_project.id)
    assert project is not None
    assert str(project.name) == "Test Project"
    assert str(project.github_url) == "https://github.com/user/test-project"

    # Test getting nonexistent project
    assert get_project(db_session, 999) is None


def test_get_projects(db_session, sample_project):
    """Test retrieving all projects."""
    # Add another project with different upvotes to test ordering
    project2 = Project(
        name="Another Project",
        github_url="https://github.com/user/another-project",
        author_name="Another User",
        module_name="another_module",
        upvotes=10,
    )
    db_session.add(project2)
    db_session.commit()

    projects = get_projects(db_session)
    assert len(projects) == 2
    # Check if ordered by upvotes (descending)
    assert int(str(projects[0].upvotes)) > int(str(projects[1].upvotes))


def test_search_projects_by_name(db_session, sample_project):
    """Test searching projects by name."""
    results = search_projects_by_name(db_session, "Test")
    assert len(results) == 1
    assert results[0].id == sample_project.id

    # Test case insensitivity
    results = search_projects_by_name(db_session, "test")
    assert len(results) == 1

    # Test no results
    results = search_projects_by_name(db_session, "nonexistent")
    assert len(results) == 0


def test_search_projects_by_author(db_session, sample_project):
    """Test searching projects by author name."""
    results = search_projects_by_author(db_session, "Test User")
    assert len(results) == 1
    assert results[0].id == sample_project.id

    # Test partial match
    results = search_projects_by_author(db_session, "User")
    assert len(results) == 1

    # Test no results
    results = search_projects_by_author(db_session, "nonexistent")
    assert len(results) == 0


def test_create_project(db_session):
    """Test creating a new project."""
    project_data = ProjectCreate(
        name="New Project",
        github_url="https://github.com/user/new-project",
        author_name="New User",
        module_name="new_module",
    )
    project = create_project(db_session, project_data)
    assert project.id is not None
    assert str(project.name) == "New Project"
    assert int(str(project.upvotes)) == 0  # Default value


def test_update_project(db_session, sample_project):
    """Test updating a project."""
    update_data = ProjectUpdate(name="Updated Project Name")
    updated_project = update_project(db_session, sample_project.id, update_data)

    assert updated_project is not None

    assert str(updated_project.name) == "Updated Project Name"
    assert str(updated_project.github_url) == sample_project.github_url  # Unchanged

    # Test updating nonexistent project
    assert update_project(db_session, 999, update_data) is None


def test_delete_project(db_session, sample_project):
    """Test deleting a project."""
    assert delete_project(db_session, sample_project.id) is True
    assert get_project(db_session, sample_project.id) is None

    # Test deleting nonexistent project
    assert delete_project(db_session, 999) is False
