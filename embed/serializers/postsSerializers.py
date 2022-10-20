def postEntity(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "text": post["text"],
        "author_id":  str(post["author_id"])
    }


def postToCreate(post) -> dict:
    return {
        "title": post["title"],
        "text": post["text"],
        "author_id":  str(post["author_id"])
    }

def postListEntity(posts) -> list:
    return [postEntity(post) for post in posts]

