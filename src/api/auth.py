from fastapi import APIRouter, HTTPException, Response, status

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и Аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с таким email не зарегистрирован",
        )
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
