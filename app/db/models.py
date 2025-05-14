from sqlalchemy import Column, Integer, String

from .base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    github_url = Column(String)
    author_name = Column(String, index=True)
    module_name = Column(String)
    upvotes = Column(Integer, default=0)
