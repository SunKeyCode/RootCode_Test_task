import os
from logging import getLogger
from logging.config import dictConfig

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from configs.app_config import DEBUG, DB_URL

# logger = getLogger("main.session")
# dictConfig(LOGGER_CONF)

# TESTING = os.environ.get("TESTING")
#
# logger.debug("TESTING_CONFIG=%s", TESTING)

# DB_URL = "postgresql+asyncpg://{user}:{password}@{host}/{db_name}".format(
#     user=app_config.DB_USER,
#     password=app_config.DB_PASSWORD,
#     host=app_config.DB_HOST,
#     db_name=app_config.DB_NAME,
# )

async_engine = create_async_engine(DB_URL, pool_size=20, echo=DEBUG)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_db_session():
    async with async_session() as session:
        yield session
