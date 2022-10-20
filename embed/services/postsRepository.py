from bson import ObjectId
from pymongo.errors import WriteError

import embed.main as embed
from embed.routers.exceptions import AlreadyExistsHTTPException, NotFoundHTTPException
from embed.schemas.posts import InsertDBPostSchema

async def insert_post(document: InsertDBPostSchema, collection: str) -> dict:
    """

    :param document:
    :param collection:
    :return:
    """
    try:
        document = await embed.app.state.mongo_collection[collection].insert_one(document)
        findOne =  await embed.app.state.mongo_collection[collection].find_one({"_id": document.inserted_id})
        return findOne
    except WriteError:
        raise AlreadyExistsHTTPException(f"Error while trying to create Post")

