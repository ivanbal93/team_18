from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    login: str
    is_admin: bool
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    id: int
    login: str
    password: str
    is_admin: bool = False
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


# class UserUpdate(schemas.BaseUserUpdate):
#     pass