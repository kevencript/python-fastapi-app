from datetime import datetime, timedelta
from bson.objectid import ObjectId
from fastapi import APIRouter, Response, status, Depends, HTTPException

from embed.utils import hash_password, verify_password
from embed import config
from embed.routers.exceptions import NotFoundHTTPException
from embed.services.repository import create_user_db, mail_exists
from embed.schemas.users import CreateUserSchema, UserResponse
from embed.serializers.userSerializers import userResponseEntity 

global_settings = config.get_settings()
collection = global_settings.collection

router = APIRouter()

ACCESS_TOKEN_EXPIRES_IN = global_settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = global_settings.REFRESH_TOKEN_EXPIRES_IN

@router.post(
    '/register',
     status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def create_user(payload: CreateUserSchema):
    """

    :param payload:
    :return:
    """
    try:
        # Check if user already exist
        mailAlreadyExist = await mail_exists(payload.email.lower(), collection)
        if mailAlreadyExist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Account already exist')

        # Compare password and passwordConfirm
        if payload.password != payload.passwordConfirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
        
        #  Hash the password
        payload.password = hash_password(payload.password)
        del payload.passwordConfirm
        payload.verified = True
        payload.email = payload.email.lower()
        payload.created_at = datetime.utcnow()

        userDict = payload.dict()

        # Inserting user into the DB
        createdUser = await create_user_db(userDict, collection)
        userToReturn = userResponseEntity(createdUser)

        return {"status": "success", "user": userToReturn}
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))

