from datetime import datetime
from typing import Any, Sequence

from sqlalchemy import func, Sequence, Row, RowMapping
from sqlalchemy.engine.result import _TP
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select

from models.models import ProjectData


class ProjectDataDBManger:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_create(self, items, file_version):
        project_items = []
        async with self.session.begin():
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

            self.session.add_all(project_items)

    async def get_by_file_version(
        self, version: int
    ) -> Sequence[Row | RowMapping | Any]:
        data = await self.session.scalars(
            select(ProjectData)
            .where(ProjectData.file_version_id == version)
            .options(joinedload(ProjectData.project))
            .order_by(ProjectData.date)
        )

        return data.all()

    async def get_report_grouped_by_date(self, **query_params) -> Sequence[Row[_TP]]:
        statement = select(
            ProjectData.date,
            func.sum(ProjectData.planed).label("plan"),
            func.sum(ProjectData.in_fact).label("fact"),
        )

        if query_params.get("type_value"):
            type_value = query_params.get("type_value")
            if type_value == "p":
                statement = select(
                    ProjectData.date,
                    func.sum(ProjectData.planed).label("plan"),
                )
            elif type_value == "f":
                statement = select(
                    ProjectData.date,
                    func.sum(ProjectData.in_fact).label("fact"),
                )

        if query_params.get("version"):
            version = query_params["version"]
            statement = statement.where(ProjectData.file_version_id == version)

        if query_params.get("year"):
            year = query_params["year"]
            start_date = datetime(year=year, month=1, day=1)
            end_date = datetime(year=year, month=12, day=31)
            statement = statement.where(
                ProjectData.date >= start_date, ProjectData.date <= end_date
            )

        result = await self.session.execute(
            statement.group_by(ProjectData.date).order_by(ProjectData.date)
        )

        return result.all()
