from datetime import datetime

from sqlalchemy import DateTime, String, Integer, ForeignKey, Float
from sqlalchemy.orm import mapped_column, Mapped

from models.base_model import ORMBaseModel


class FileVersion(ORMBaseModel):
    __tablename__ = "file_version"

    filename = mapped_column(String, nullable=False)
    upload_date = mapped_column(DateTime, default=datetime.now)


class Project(ORMBaseModel):
    __tablename__ = "project"

    name = mapped_column(String, nullable=False)
    code = mapped_column(Integer, nullable=False, unique=True)


class ProjectData(ORMBaseModel):
    __tablename__ = "project_data"
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id"),
        nullable=False,
    )
    file_version_id: Mapped[int] = mapped_column(
        ForeignKey("file_version.id"),
        nullable=False,
    )
    date = mapped_column(DateTime, nullable=False)
    planed = mapped_column(Float, nullable=True)
    in_fact = mapped_column(Float, nullable=True)
