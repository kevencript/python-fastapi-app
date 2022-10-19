from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from embed import config
from embed.routers import router as v1
from embed.services.repository import get_mongo_meta
from embed.utils import get_logger, init_mongo

global_settings = config.get_settings()

if global_settings.environment == "local":
    get_logger("uvicorn")

app = FastAPI()

origins = [
    global_settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    app.state.logger = get_logger(__name__)
    app.state.logger.info("Starting Embed API...")
    app.state.mongo_client, app.state.mongo_db, app.state.mongo_collection = await init_mongo(
        global_settings.db_name, global_settings.db_url, global_settings.collection
    )


@app.on_event("shutdown")
async def shutdown_event():
    app.state.logger.info("Stopping Embed web service...")


@app.get("/health-check")
async def health_check():
    # # TODO: check settings dependencies passing as args and kwargs
    # a = 5
    # try:
    #     assert 5 / 0
    # except Exception:
    #     app.state.logger.exception("My way or highway...")
    return await get_mongo_meta()
