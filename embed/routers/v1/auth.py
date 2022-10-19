from os import access
from fastapi import APIRouter, Response, status, Depends, HTTPException
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from embed import config

from embed.utils import hash_password, verify_password
from embed.routers.exceptions import NotFoundHTTPException
from embed.services.repository import create_user_db, mail_exists, retrieve_document
from embed.serializers.userSerializers import userResponseEntity, userEntity
from embed.schemas.users import LoginUserSchema,CreateUserSchema, UserResponse
from embed.oauth2 import AuthJWT, require_user

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
async def create_user(payload: CreateUserSchema, Authorize: AuthJWT = Depends()):
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
        userToReturn = userResponseEntity(createdUser) # Serialized pattern for return

        # Create access token
        access_token = Authorize.create_access_token(
            subject=str(userToReturn["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
       
        return {"status": "success", "access_token":access_token, "user": userToReturn}
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))


@router.post('/login', status_code=status.HTTP_200_OK, )
async def login(payload: LoginUserSchema, Authorize: AuthJWT = Depends()):
    """

    :param payload:
    :param response:
    :param Authorize:
    :return:
    """
    try:

        notSerializedUser = await mail_exists(payload.email.lower(), collection)
        if not notSerializedUser:
            raise NotFoundHTTPException('Incorrect Email or Password')

        # Check if the user exist
        user = userEntity(notSerializedUser)

        # Check if the password is valid
        if not verify_password(payload.password, user['password']):
            raise NotFoundHTTPException('Incorrect Email or Password')

        # Create access token
        access_token = Authorize.create_access_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
       
        # Send both access
        return {'status': 'success', 'access_token': access_token}
        
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))

@router.get('/profile', status_code=status.HTTP_200_OK)
async def protected(user_id: str = Depends(require_user)):
    userAccount = await retrieve_document(document_id=user_id, collection=collection)
    return userResponseEntity(userAccount)
