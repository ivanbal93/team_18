import uvicorn

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from src.database import User

from src.authentication.config import auth_backend
from src.authentication.manager import get_user_manager
from src.authentication.schemas import UserRead, UserCreate

from src.core.routers import site_router, category_router, news_router


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title="Parsing Application"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authentication"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(site_router)
app.include_router(category_router)
app.include_router(news_router)



#здесь можно будет добавить в параметрах свойства юзера для определения наличия/отсуствия роли админа
current_user = fastapi_users.current_user()


@app.get("/protected_route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.login}"
