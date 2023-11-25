from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    text: str
    like: int
    repost: int
    site_id: int
    url: str

    class Config:
        orm_mode = True


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    pass


class CommentBase(BaseModel):
    text: str

    class Config:
        orm_model = True


class CommentCreate(CommentBase):
    pass
