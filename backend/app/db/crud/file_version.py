from sqlalchemy.ext.asyncio import AsyncSession

from models.models import FileVersion


class FileVersionDBManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, filename):
        async with self.session.begin():
            file_version = FileVersion(filename=filename)
            self.session.add(file_version)

        return file_version
