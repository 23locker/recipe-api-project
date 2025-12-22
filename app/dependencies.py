from fastapi import Depends
from tortoise.exceptions import DoesNotExist

from app.models.tortoise.user import User
from app.utils.security import verify_token


async def get_current_user(token: str = Depends(verify_token)) -> User:
    try:
        user = await User.get(id=token["user_id"])
        return user
    except DoesNotExist:
        raise Exception("User not found")
