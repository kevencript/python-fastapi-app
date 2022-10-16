from bson import ObjectId
from pymongo.errors import WriteError

import embed.main as embed
from embed.routers.exceptions import AlreadyExistsHTTPException

async def get_mongo_meta() -> dict:
    list_databases = await embed.app.state.mongo_client.list_database_names()
    list_of_collections = {}
    for db in list_databases:
        list_of_collections[db] = await embed.app.state.mongo_client[db].list_collection_names()
    mongo_meta = await embed.app.state.mongo_client.server_info()
    return {"version": mongo_meta["version"], "databases": list_databases, "collections": list_of_collections}
