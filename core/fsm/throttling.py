from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import Message, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any],
                       ) -> Any:
        user = f"user{event.from_user.id}"

        check_user = await self.storage.redis.get(name=user)

        if check_user and str(event.chat.id):
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=0, ex=2)
                return await event.answer("Не нужно так часто отправлять сообщения, вас много, а я один()")
            return
        await self.storage.redis.set(name=user, value=1, ex=2)

        return await handler(event, data)
