from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import models
from models.models import Project, FileVersion, ProjectData


async def check_projects(session: AsyncSession, codes: list):
    projects = await session.scalars(
        select(Project.code).where(Project.code.in_(codes))
    )
    await session.commit()

    return projects.all()


async def create_file_version(session: AsyncSession, filename):
    async with session.begin():
        file_version = FileVersion(filename=filename)
        session.add(file_version)

    return file_version


async def create_projects(session: AsyncSession, projects_data: list[list]):
    projects = []
    async with session.begin():
        for item in projects_data:
            code, name = item
            project = Project(name=name, code=code)
            projects.append(project)

        session.add_all(projects)


async def create_product_data_items(session: AsyncSession, items, file_version):
    project_items = []
    async with session.begin():
        for item in items:
            for data_item in item["data"]:
                project_data = ProjectData(
                    project_id=item["code"],
                    file_version_id=file_version,
                    date=data_item[0],
                    planed=data_item[1],
                    in_fact=data_item[2],
                )
                project_items.append(project_data)

        session.add_all(project_items)
