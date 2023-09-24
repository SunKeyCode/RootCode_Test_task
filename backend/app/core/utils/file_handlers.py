import os
from pathlib import Path

import aiofiles
from configs.app_config import FILES_DIR


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
