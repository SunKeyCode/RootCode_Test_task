import os
from collections import OrderedDict
from pathlib import Path

import aiofiles
from configs.app_config import FILES_DIR
from models.models import ProjectData


async def save_file_to_filesystem(filename: str, content: bytes) -> Path:
    upload_path = FILES_DIR / "uploaded"
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        # logger.debug("Created path: %s", app_config.MEDIA_ROOT / link)

    file_name = upload_path / filename

    async with aiofiles.open(
        file=file_name,
        mode="wb",
    ) as file_to_write:
        await file_to_write.write(content)

    return file_name


def convert_orm_data_to_dict(data: list[ProjectData]) -> dict:
    result_dict = {}
    for item in data:
        project = result_dict.setdefault(item.project_id, {})
        project["name"] = item.project.name
        proj_data = project.setdefault("data", OrderedDict())
        project_data_as_string = str(item.date.date())
        date = proj_data.setdefault(project_data_as_string, {})
        date["in_fact"] = item.in_fact
        date["planed"] = item.planed

    return result_dict