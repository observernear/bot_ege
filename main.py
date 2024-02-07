from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
# from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand

import logging
import contextlib
import asyncio

from core.handlers.basic import *
from core.handlers.callback import *
from core.fsm.state import FSMsubject

import config as cfg


async def start():

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    bot: Bot = Bot(token=cfg.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.message.register(command_start, Command("start"))
    dp.message.register(command_start, Command("restart"))
    dp.message.register(make_test_message, FSMsubject.problems)

    dp.callback_query.register(
        choose_subject_callback, F.data.in_(["math", "rus", "inf"]))
    dp.callback_query.register(
        material_test_callback, FSMsubject.subject)
    dp.callback_query.register(callback_handler, F.data)

    bot_commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/restart",
                   description="Перезапустить бота, если что-то пошло не так")
    ]

    await bot.set_my_commands(bot_commands)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
