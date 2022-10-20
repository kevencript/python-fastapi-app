from array import array
from pydantic import BaseModel, Field, constr
from bson.errors import InvalidId
from bson import ObjectId

class ObjectIdField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        try:
            return ObjectId(str(value))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")

class PostBaseSchema(BaseModel):
    title: constr(max_length=100)
    text: constr(max_length=1000)

    class Config:
        orm_mode = True

class CreatePostSchema(PostBaseSchema):
    title: constr(max_length=100)
    text: constr(max_length=1000)

class SearchPersonalPostSchema(BaseModel):
    string_match: constr(max_length=100)
    
class InsertDBPostSchema(PostBaseSchema):
    author_id: ObjectIdField = Field(...)

class PostResponseSchema(PostBaseSchema):
    id: str
    author_id: str
    pass

class PostResponse(BaseModel):
    status: str
    post: PostResponseSchema

class PostListResponse(BaseModel):
    posts: list

class PostListSchema(PostBaseSchema):
    posts: list
    