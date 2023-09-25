from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.models import Project


class ProjectDBManager:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_projects(self, codes: list[int]):
        projects = await self.session.scalars(
            select(Project.code).where(Project.code.in_(codes))
        )
        await self.session.commit()

        return projects.all()

    async def create(self, project_list: list[list]):
        projects = []
        async with self.session.begin():
            for item in project_list:
                code, name = item
                project = Project(name=name, code=code)
                projects.append(project)

            self.session.add_all(projects)
