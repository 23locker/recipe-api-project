from fastapi import APIRouter, HTTPException, status

from app.schemas.user import Token, UserLogin, UserRegister, UserResponse
from app.services import auth_service
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])
auth_service = AuthService()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    """
    Регистрация нового пользователя
    """
    user = await auth_service.register_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    return user


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """
    Вход пользователя в систему
    """
    result = await auth_service.login_user(
        username=user_data.username,
        password=user_data.password,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return result
