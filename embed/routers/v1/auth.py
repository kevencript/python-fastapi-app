from fastapi import APIRouter, Response, status, Depends, HTTPException
from datetime import datetime, timedelta
from bson.objectid import ObjectId

from embed import config

from embed.utils import hash_password, verify_password
from embed.routers.exceptions import NotFoundHTTPException
from embed.services.repository import create_user_db, mail_exists
from embed.serializers.userSerializers import userResponseEntity, userEntity
from embed.schemas.users import LoginUserSchema,CreateUserSchema, UserResponse
from embed.schemas.oauth2 import AuthJWT, require_user

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
        userToReturn = userResponseEntity(createdUser) # Serialized pattern for return

        return {"status": "success", "user": userToReturn}
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(payload: LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
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

        # Create refresh token
        refresh_token = Authorize.create_refresh_token(
            subject=str(user["id"]), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

        # Store refresh and access tokens in cookie
        response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
        response.set_cookie('refresh_token', refresh_token,
                            REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
        response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

        # Send both access
        return {'status': 'success', 'access_token': access_token}
    except ValueError as exception:
        raise NotFoundHTTPException(msg=str(exception))

@router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends(require_user)):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}
