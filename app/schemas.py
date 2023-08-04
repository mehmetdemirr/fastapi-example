from datetime import datetime
from pydantic import BaseModel,EmailStr


class UserModel(BaseModel):
    id:int
    email:EmailStr | str
    created_at:datetime | None=None
    token:str | None= None

    class Config:
        from_attributes=True

class InUserModel(UserModel):
    password:str

    class Config:
        from_attributes=True


class PostModel(BaseModel):
    title: str
    content:str
    published:bool = True
    owner:UserModel

    class Config:
        from_attributes=True

class Token(BaseModel):
    token: str | None=None
    mail:str | None=None
    