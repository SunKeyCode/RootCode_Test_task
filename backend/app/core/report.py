import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from models.models import ProjectData


async def report_query(session: AsyncSession, **query_params):
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
        start_date = datetime.datetime(year=year, month=1, day=1)
        end_date = datetime.datetime(year=year, month=12, day=31)
        statement = statement.where(
            ProjectData.date >= start_date, ProjectData.date <= end_date
        )

    result = await session.execute(statement.group_by(ProjectData.date))

    return result.all()
