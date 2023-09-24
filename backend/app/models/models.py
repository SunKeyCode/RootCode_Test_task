from datetime import datetime

from sqlalchemy import DateTime, String, Integer, ForeignKey, Float, Identity
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base_class import Base


class FileVersion(Base):
    __tablename__ = "file_version"

    id = mapped_column(Integer, Identity(always=True), primary_key=True)
    filename = mapped_column(String, nullable=False)
    upload_date = mapped_column(DateTime, default=datetime.now)


class Project(Base):
    __tablename__ = "project"

    # id = mapped_column(Integer, Identity(always=True), primary_key=True)
    code = mapped_column(Integer, nullable=False, primary_key=True)
    name = mapped_column(String, nullable=False)


class ProjectData(Base):
    __tablename__ = "project_data"

    id = mapped_column(Integer, Identity(always=True), primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.code"),
        nullable=False,
    )
    file_version_id: Mapped[int] = mapped_column(
        ForeignKey("file_version.id"),
        nullable=False,
    )
    date = mapped_column(DateTime, nullable=False)
    planed = mapped_column(Float, nullable=True)
    in_fact = mapped_column(Float, nullable=True)

    project: Mapped["Project"] = relationship(
        lazy="raise"
    )
