from typing import Any, Dict, Optional

from tortoise.exceptions import DoesNotExist

from app.models.tortoise.user import User
from app.utils.security import create_access_token, hash_password, verify_password


class AuthService:
    async def register_user(
        self, username: str, email: str, password: str
    ) -> Optional[User]:
        """
        Регистрация нового пользователя
        """
        try:
            await User.get(username=username)
            return None
        except DoesNotExist:
            user = await User.create(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role="user",
            )
            return user

    async def login_user(
        self, username: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """
        Вход пользователя
        """
        try:
            user = await User.get(username=username)

            if not verify_password(password, user.password_hash):
                return None

            if not user.is_active:
                return None

            access_token = create_access_token(data={"user_id": user.id})

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            }
        except DoesNotExist:
            return None

    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Получение пользователя по его ID
        """
        try:
            return await User.get(id=user_id)
        except DoesNotExist:
            return None
