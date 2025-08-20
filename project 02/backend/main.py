# from routers.r_test import router as test_router
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import Body, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
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


# Define a custom function to generate unique operation IDs for OpenAPI routes
def custom_generate_unique_id_function(route: APIRoute) -> str:
    # Use the route's name as its unique identifier
    return route.name


# Create a FastAPI application instance with custom metadata and documentation settings
app = FastAPI(
    title="Ventuno API",
    version="1.0.0",
    description="API for managing sellers, delivery partners, shipments, and more.",
    # Server start/stop listener
    lifespan=lifespan_handler,
    docs_url="/",
    redoc_url=None,  # Disable ReDoc documentation at /redoc
    generate_unique_id_function=custom_generate_unique_id_function,  # Use custom function for OpenAPI operation IDs
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def add_log(log: str) -> None:
    with open("file.log", "a") as file:
        file.write(f"{log}\n")


# Add custom middleware
@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start = perf_counter()

    response: Response = await call_next(request)

    end = perf_counter()
    time_taken = round(end - start, 2)

    add_log(f"{request.method} {request.url} ({response.status_code}) {time_taken} s")
    # add_log.delay(
    #     f"{request.method} {request.url} ({response.status_code}) {time_taken} s"
    # )

    return response


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
    # sellerAuth token url routes
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

    # partnerAuth token url routes
    openapi_schema["paths"]["/shipmentv3/"]["patch"]["security"] = [{"partnerAuth": []}]
    openapi_schema["paths"]["/shipmentv3/v2"]["patch"]["security"] = [
        {"partnerAuth": []}
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


# Scalar API Documentation


# Define a GET endpoint at /scalar  that is excluded from the OpenAPI schema
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    # Return the Scalar API reference using the app's OpenAPI URL and a custom title
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


@app.get("/healthy")
def health_check():
    return {"status": "HEALTHY"}


@app.get("/healthy2")
async def health_check2():
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
