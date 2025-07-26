# from routers.r_test import router as test_router
from contextlib import asynccontextmanager

from fastapi import Body, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from scalar_fastapi import get_scalar_api_reference
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from .db.async_engine_sqlmodel_postgres import create_db_tables
from .routers.r_delivery_partner import router as delivery_prtner_router
from .routers.r_seller import router as seller_router
from .routers.r_shipment import router as shimpent_router

# from .routers.r_shipmentV2 import router as shimpentV2_router
from .routers.r_shipmentV3 import router as shimpentV3_router
from .routers.r_test import router as test_router
from .utils.token import oauth2_scheme_partner, oauth2_scheme_seller


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(
    title="Ventuno API",
    version="1.0.0",
    description="API for managing sellers, delivery partners, shipments, and more.",
    # Server start/stop listener
    lifespan=lifespan_handler,
)


# 🧠 Inject custom Swagger security schemes
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "sellerAuth": {
            "type": "oauth2",
            "flows": {"password": {"tokenUrl": "/seller/token", "scopes": {}}},
        },
        "partnerAuth": {
            "type": "oauth2",
            "flows": {"password": {"tokenUrl": "/partner/token", "scopes": {}}},
        },
    }
    # if "/partner/update" in openapi_schema.get("paths", {}):
    #     if "post" in openapi_schema["paths"]["/partner/update"]:
    #         openapi_schema["paths"]["/partner/update"]["post"]["security"] = [
    #             {"partnerAuth": []}
    #         ]

    # Optional: make endpoints require auth by default in Swagger
    openapi_schema["security"] = [{"sellerAuth": []}, {"partnerAuth": []}]
    openapi_schema["paths"]["/seller/dashboardv2"]["get"]["security"] = [
        {"sellerAuth": []}
    ]
    openapi_schema["paths"]["/shipmentv3/"]["get"]["security"] = [{"sellerAuth": []}]
    openapi_schema["paths"]["/shipmentv3/v2/"]["get"]["security"] = [{"sellerAuth": []}]
    openapi_schema["paths"]["/shipmentv3/cancel"]["get"]["security"] = [
        {"sellerAuth": []}
    ]
    openapi_schema["paths"]["/shipmentv3/cancel/v2"]["get"]["security"] = [
        {"sellerAuth": []}
    ]
    openapi_schema["paths"]["/shipmentv3/"]["post"]["security"] = [{"sellerAuth": []}]
    openapi_schema["paths"]["/shipmentv3/v2/"]["post"]["security"] = [
        {"sellerAuth": []}
    ]
    openapi_schema["paths"]["/seller/logout"]["get"]["security"] = [{"sellerAuth": []}]
    openapi_schema["paths"]["/partner/logout"]["get"]["security"] = [
        {"partnerAuth": []}
    ]
    openapi_schema["paths"]["/partner/update"]["post"]["security"] = [
        {"partnerAuth": []}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

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
app.include_router(seller_router, prefix="/seller", tags=["seller"])
app.include_router(delivery_prtner_router, prefix="/partner", tags=["Delivery Partner"])
app.include_router(shimpentV3_router, prefix="/shipmentv3", tags=["shipment v3"])
# app.include_router(shimpentV2_router, prefix="/shipmentV2", tags=["shipment v2"])
app.include_router(test_router, prefix="/test", tags=["test"])


# If you use alembic, you can ignore below line
# models.Base.metadata.create_all(engine)


# @app.get("/")
# async def root():
#     return RedirectResponse(url="/todo", status_code=status.HTTP_302_FOUND)
