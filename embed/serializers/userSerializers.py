def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "verified": user["verified"],
        "password": user["password"],
        "created_at": user["created_at"],

    }


def userResponseEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "created_at": user["created_at"],

    }


def embeddedUserResponse(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
    }


def userListEntity(users) -> list:
    return [userEntity(user) for user in users]

