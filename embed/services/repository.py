from datetime import date
from bson import ObjectId
from pymongo.errors import WriteError

import embed.main as embed
from embed.routers.exceptions import AlreadyExistsHTTPException, NotFoundHTTPException

async def retrieve_document(document_id: str, collection: str) -> dict:
    """

    :param document_id:
    :param collection:
    :return:
    """
    document_filter = {"_id": ObjectId(document_id)}
    if document := await embed.app.state.mongo_collection[collection].find_one(document_filter):
        return document
    else:
        raise ValueError(f"No document found for {document_id=} in {collection=}")

async def mail_exists(email: str, collection: str) -> dict:
    """

    :param email:
    :param collection:
    :return:
    """
    document_filter = {"email": email}
    if document := await embed.app.state.mongo_collection[collection].find_one(document_filter):
        return document
    else:
        return False

async def create_user_db(document: dict, collection: str) -> dict:
    """

    :param document:
    :param collection:
    :return:
    """
    try:
        document = await embed.app.state.mongo_collection[collection].insert_one(document)
        return await retrieve_document(document.inserted_id, collection)
    except WriteError:
        raise NotFoundHTTPException("Error while creating the user")


async def create_document(document: dict, collection: str) -> dict:
    """

    :param document:
    :param collection:
    :return:
    """
    try:
        document = await embed.app.state.mongo_collection[collection].insert_one(document)
        return await retrieve_document(document.inserted_id, collection)
    except WriteError:
        raise AlreadyExistsHTTPException(f"Document with {document.inserted_id=} already exists")


async def get_mongo_meta() -> dict:
    list_databases = await embed.app.state.mongo_client.list_database_names()
    list_of_collections = {}
    for db in list_databases:
        list_of_collections[db] = await embed.app.state.mongo_client[db].list_collection_names()
    mongo_meta = await embed.app.state.mongo_client.server_info()
    return {"version": mongo_meta["version"], "databases": list_databases, "collections": list_of_collections}
