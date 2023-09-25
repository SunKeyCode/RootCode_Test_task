from sqlalchemy.ext.asyncio import AsyncSession

from core.excel.reader import PandasDataLoader
from db.crud.project import ProjectDBManager


async def check_and_create_projects(
    session: AsyncSession, loader: PandasDataLoader
) -> None:
    db_manager = ProjectDBManager(session=session)
    projects = await db_manager.get_projects(loader.codes)
    set_ids_to_create = set(loader.codes).difference(set(projects))
    proj_to_create = loader.get_projects_info_by_codes(list(set_ids_to_create))
    if len(proj_to_create):
        await db_manager.create(proj_to_create)
