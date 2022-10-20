from fastapi import APIRouter, Response, status, Depends, HTTPException

from embed import config

from embed.routers.exceptions import InternalServerErrorHTTPException, NotFoundHTTPException
from embed.services.postsRepository import insert_post, get_self_posts_db
from embed.serializers.postsSerializers import postToCreate, postEntity, postListEntity
from embed.schemas.posts import PostResponse, CreatePostSchema, PostListResponse, SearchPersonalPostSchema
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
        return { 'status': "Post successfully created", 'post': postEntity(createdPost)}

    except ValueError as exception:
        raise InternalServerErrorHTTPException(msg=str(exception))

@router.post(
    '/search',
    status_code=status.HTTP_200_OK,
    response_model=PostListResponse
)
async def get_self_posts(payload: SearchPersonalPostSchema, user_id: str = Depends(require_user)):
    """
    :param payload:
    :param user_id:
    :return:
    """
    try:
        
        userPosts = await get_self_posts_db(str(payload.string_match), user_id, collection)
        if not userPosts:
            return []

        return { 'posts': postListEntity(userPosts) }

    except ValueError as exception:
        raise InternalServerErrorHTTPException(msg=str(exception))
