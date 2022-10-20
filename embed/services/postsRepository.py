import re
from pymongo.errors import WriteError

import embed.main as embed
from embed.routers.exceptions import InternalServerErrorHTTPException
from embed.schemas.posts import InsertDBPostSchema, SearchPersonalPostSchema

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
        raise InternalServerErrorHTTPException(f"Error while trying to create Post")

async def get_self_posts_db(string_match: str,  user_id: str, collection: str) -> dict:
    """

    :param string_match:
    :param user_id:
    :param collection:
    :return:
    """ 
    try:
        term_list = [string_match] # Can be increased to receive more than one String Match
        regexp = re.compile(r"|".join(term_list), re.IGNORECASE)
        return await embed.app.state.mongo_collection[collection].find({"title": regexp, 'author_id': user_id }).to_list(length=None)
    except WriteError:
        raise InternalServerErrorHTTPException(f"Error while trying to return user Posts")
