from pydantic import BaseModel


class CategoryNewsCreate(BaseModel):
    category_id: int
    news_id: int

    class Config:
        orm_mode = True


class CategorySiteCreate(BaseModel):
    category_id: int
    site_id: int

    class Config:
        orm_mode = True