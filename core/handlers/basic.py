from aiogram import Bot
from aiogram.types import Message, callback_query, InputMediaDocument
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from time import sleep
from datetime import datetime


import os

from db import db
from core.keyboards.inline import *
from test import get_test


async def command_start(message: Message, bot: Bot):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id, text="Привет, меня зовут Сотка. Я бот, который поможет тебе с ЕГЭ. Вот что я умею:", reply_markup=main_inline_keyboard())


async def make_test_message(message: Message, bot: Bot, state: FSMContext):
    subjects = await state.get_data()
    subject = subjects["subject"]
    problems = message.text.strip().replace("-", " ").split(" ")
    dicts = {}
    for i in range(len(problems)):
        try:
            if i % 2 == 0:
                if (subject == 'math' and int(problems[i]) > 19) or (subject == 'rus' and int(problems[i]) > 27) or (subject == 'inf' and int(problems[i]) > 27) or (subject == 'phys' and int(problems[i]) > 26):
                    raise Exception
                dicts[int(problems[i])] = int(problems[i + 1])
        except Exception as e:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Ты ввел задания неправильно. Попробуй ещё раз!"
            )
            return
    reply_message = await message.reply("Хороший выбор, сейчас все будет 👌")
    try:
        save_path, save_path_solutions = get_test(
            subject=str(subject), problems=dicts)
        documents = [InputMediaDocument(media=FSInputFile(path=str(save_path), filename="задания.pdf")), InputMediaDocument(media=FSInputFile(
            path=str(save_path_solutions), filename="решения.pdf"))]
        await bot.send_media_group(chat_id=message.from_user.id, media=documents)
    except Exception:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Ой-ой, ты что-то не то ввел. Давай сначала!"
        )
        return
    finally:
        await bot.delete_message(chat_id=reply_message.chat.id, message_id=reply_message.message_id)
    try:
        os.remove(save_path)
        os.remove(save_path_solutions)
    except:
        pass
    await state.clear()
    msg = ''
    date = db.get_date_test(message.from_user.id)
    now_date = str(datetime.now().day)
    if date != now_date:
        db.update_date_test(message.from_user.id, now_date)
        db.update_ball(message.from_user.id, 10)
        msg = '\n\n<i>Тебе начислено 10 баллов за вариант</i>'
    await bot.send_message(chat_id=message.chat.id, text="Продолжим?"+msg, reply_markup=main_inline_keyboard())
