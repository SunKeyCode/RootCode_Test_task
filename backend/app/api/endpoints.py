from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.core import PandasDataLoader
from core.file_unload import select_file_data, create_file_from_data, write_exel
from core.projects import (
    check_projects,
    create_file_version,
    create_projects,
    create_product_data_items,
)
from core.report import report_query
from core.utils.file_handlers import save_file_to_filesystem
from db.session import get_db_session

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
    proj = await check_projects(session=session, codes=loader.codes)
    diff = set(loader.codes).difference(set(proj))
    proj_to_create = loader.get_projects_info_by_codes(list(diff))
    await create_projects(session, proj_to_create)
    file_version = await create_file_version(
        session=session, filename=full_path.as_posix()
    )
    await create_product_data_items(session, loader.get_items_for_db(), file_version.id)
    return {
        "filename": full_path,
        "dates": loader.dates,
        "codes": loader.codes,
        "proj": proj,
        "file_version": file_version.id,
    }


@router.get("/unload/{version_id}")
async def unload_file(
    version_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    data = await select_file_data(session, version_id)
    to_excel = create_file_from_data(data)
    file_name = write_exel(to_excel)
    return FileResponse(
        file_name,
        filename="result.xlsx",
        media_type="multipart/form-data",
    )


@router.get("/report")
async def get_report(
    year: int | None = None,
    version: int | None = None,
    type_value: Annotated[str | None, Query(pattern="^[pf]$")] = None,
    session: AsyncSession = Depends(get_db_session),
):
    result = await report_query(
        session,
        year=year,
        version=version,
        type_value=type_value,
    )
    res = []
    for item in result:
        item_dict = {
            "date": item.date,
            "plan": item.plan,
            "fact": item.fact,
        }
        res.append(item_dict)
    return {
        "result": res,
    }
