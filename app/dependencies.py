from fastapi import Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.models.tortoise.user import User
from app.utils.security import verify_token


async def get_current_user(token: dict = Depends(verify_token)) -> User:
    """
    Получить текущего пользователя по JWT токену
    """
    try:
        user = await User.get(id=token["user_id"])

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive"
            )

        return user

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Получить текущего пользователя с проверкой, что он администратор
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can access this resource",
        )

    return current_user
