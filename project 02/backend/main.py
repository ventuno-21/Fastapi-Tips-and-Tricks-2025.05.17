from fastapi import FastAPI, Body
from scalar_fastapi import get_scalar_api_reference

from .routers.r_test import router as test_router
from .routers.r_shipment import router as shimpent_router
from .routers.r_shipmentV2 import router as shimpentV2_router
from .routers.r_shipmentV3 import router as shimpentV3_router

from .db.async_engine_sqlmodel_postgres import create_db_tables

# from routers.r_test import router as test_router
from contextlib import asynccontextmanager
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(
    # Server start/stop listener
    lifespan=lifespan_handler,
)


# models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, title="Scalar API 2222"
    )


@app.get("/healthy")
def health_check():
    return {"status": "HEALTHY"}


# app.include_router(shimpent_router, prefix="/shipment", tags=["shipment"])
# app.include_router(shimpentV2_router, prefix="/shipmentV2", tags=["shipment v2"])
app.include_router(shimpentV3_router, prefix="/shipmentV3", tags=["shipment v3"])
app.include_router(test_router, prefix="/test", tags=["test"])


# If you use alembic, you can ignore below line
# models.Base.metadata.create_all(engine)


# @app.get("/")
# async def root():
#     return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)
