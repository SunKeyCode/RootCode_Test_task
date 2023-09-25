from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from core.excel.reader import PandasDataLoader
from core.excel.writer import write_excel
from core.projects import check_and_create_projects
from core.utils.utils import save_file_to_filesystem, convert_orm_data_to_dict
from db.crud.file_version import FileVersionDBManager
from db.crud.project_data import ProjectDataDBManger
from db.session import get_db_session
from models.models import FileVersion, ProjectData
from schemas.project_data import ReportModel

router = APIRouter()


@router.post("/upload/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_db_session),
):
    full_path = await save_file_to_filesystem(
        filename=file.filename,
        content=await file.read(),
    )
    loader = PandasDataLoader(full_path)
    await check_and_create_projects(session, loader)

    file_version: FileVersion = await FileVersionDBManager(session=session).create(
        filename=full_path.as_posix()
    )
    await ProjectDataDBManger(session).bulk_create(
        loader.get_items_for_db(), file_version.id
    )
    return {
        "result": True,
        "file_version": file_version.id,
    }


@router.get("/download/{version_id}")
async def unload_file(
    version_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    data: list[ProjectData] = await ProjectDataDBManger(session).get_by_file_version(
        version_id
    )
    if not data:
        raise HTTPException(status_code=404, detail="file version not found")

    to_excel: dict = convert_orm_data_to_dict(data)
    file_name = write_excel(to_excel)

    return FileResponse(
        file_name,
        filename="result.xlsx",
        media_type="multipart/form-data",
    )


@router.get(
    "/report", response_model=list[ReportModel], response_model_exclude_unset=True
)
async def get_report(
    year: int | None = None,
    version: int | None = None,
    type_value: Annotated[str | None, Query(pattern="^[pf]$")] = None,
    session: AsyncSession = Depends(get_db_session),
):
    result = await ProjectDataDBManger(session).get_report_grouped_by_date(
        year=year,
        version=version,
        type_value=type_value,
    )

    return result
