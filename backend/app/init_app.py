from fastapi import FastAPI

from api.endpoints import router


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.include_router(router, prefix="/api")

    return app
