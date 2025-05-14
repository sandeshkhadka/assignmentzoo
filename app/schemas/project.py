from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    github_url: str
    author_name: str
    module_name: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    github_url: str | None = None
    author_name: str | None = None
    module_name: str | None = None


class Project(ProjectBase):
    id: int
    upvotes: int

    class Config:
        orm_mode = True
        from_attributes = True
