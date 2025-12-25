from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import Token, UserLogin, UserRegister, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])
service = AuthService()


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    """
    Регистрация нового пользователя
    """
    user = await service.register_user(
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
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Вход пользователя в систему
    """
    result = await service.login_user(
        username=form_data.username,
        password=form_data.password,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return result
