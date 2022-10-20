from os import access
from fastapi import APIRouter, Response, status, Depends, HTTPException


from embed import config

from embed.routers.exceptions import NotFoundHTTPException
from embed.services.postsRepository import insert_post
from embed.serializers.postsSerializers import postToCreate, postEntity
from embed.schemas.posts import PostResponse, CreatePostSchema
from embed.oauth2 import require_user

global_settings = config.get_settings()
collection = global_settings.collection

router = APIRouter()

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse
)
async def create_post(payload: CreatePostSchema, user_id: str = Depends(require_user)):
    """

    :param payload:
    :param user_id:
    :return:
    """
    try:
        postToSerialize = {
            'title': payload.title,
            'text': payload.text,
            'author_id': user_id
        }
        # Serializing and creating Post
        postSerialized = postToCreate(postToSerialize)
        
        createdPost = await insert_post(postSerialized, collection)
        
        return { 'status': "created", 'post': postEntity(createdPost)}

    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))