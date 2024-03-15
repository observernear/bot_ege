from aiogram import Bot
from aiogram.types import CallbackQuery, InputMediaDocument
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from random import randint
from datetime import datetime
import os


from db import db
from core.keyboards.inline import *
from core.fsm.state import *
from test import get_test


async def callback_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    msg = ''
    if callback.data == "profile":
        user_date = db.get_date(callback.from_user.id)
        if user_date != str(datetime.now().day):
            up_ball = randint(2, 4)
            db.update_date(callback.from_user.id, datetime.now().day)
            db.update_ball(callback.from_user.id, up_ball)
            msg = f'<i>Тебе начислено {up_ball} балла за посещение</i>'
        rating = db.get_num_rating(callback.from_user.id)
        ball = db.get_ball(callback.from_user.id)
        msg = f"<b>Профиль</b>\n\n•Твой ID: {callback.from_user.id}\n•Твое место в рейтинге: {rating}\n•Твой балл: {ball}\n\n" + msg
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=msg, reply_markup=main_cancel_inline_keyboard())

    # elif callback.data == "info":
    #     await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="<b>ФУНКЦИОНАЛ</b>\n-Ты можешь посмотреть свои баллы и рейтинг.\n-Я могу составлять персональные варианты <u>ЕГЭ</u>, а также давать случайные.\n-У меня есть полезные материалы для тебя.\n\n<b>БАЛЛЫ</b>\n-Баллы начисляются за ежедневные посещения вкладки 'Профиль 👤', может быть начислено от двух баллов до четырех баллов.\n-Баллы начисляются раз в день за составенный мною вариант(10 баллов).\n\n<b>РЕЙТИНГ</b>\n-Рейтинг - это твое место среди всех пользователей, ты можешь соревноваться с друзьями и всегда стремиться к первому месту!", reply_markup=main_cancel_inline_keyboard())

    elif callback.data == "choose_subject":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Хорошо, выбери предмет", reply_markup=choose_subject_inline_keyboard())

    elif callback.data == "back_main":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Чем займёмся?", reply_markup=main_inline_keyboard())
        try:
            await state.clear()
        except:
            pass

    elif callback.data == "donate":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Введите сумму в USDT:")
        await state.set_state(FSMuser.donate)


async def material_test_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    subjects = await state.get_data()
    subject = subjects["subject"]
    if callback.data == "material":
        path = list(os.walk(f"files/materials/{subject}"))
        documents = []
        for i in path[0][2]:
            if len(documents) == 10:
                await bot.send_media_group(
                    chat_id=callback.message.chat.id, media=documents
                )
                documents = []
            documents.append(InputMediaDocument(media=FSInputFile(
                path=f"files/materials/{subject}/{i}", filename=i
            )))
        await bot.send_media_group(chat_id=callback.message.chat.id, media=documents)
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        answer = ['Вот держи!', 'Специально для тебя собирал)',
                  'Для тебя ничего не жалко XP', 'Вот твой материал.']
        await bot.send_message(chat_id=callback.message.chat.id, text=f'{answer[randint(0, 3)]}\n<b>Что дальше?</b>', reply_markup=main_inline_keyboard())
        await state.clear()
    elif callback.data == "make_test":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Чтобы я смог составить персональный вариант, ты должен отправить мне какие задания ты хочешь и сколько их должно быть в варианте. \n\n<i>Пример: 1-2 3-4 12-1</i>\nЭто значит, что я составлю для тебя вариант с двумя заданиями №1, с четырьмя заданиями №3 и одним заданием №12", reply_markup=main_cancel_inline_keyboard())
        await state.set_state(FSMsubject.problems)
    elif callback.data == "random_test":
        msg = ''
        date = db.get_date_test(callback.from_user.id)
        now_date = str(datetime.now().day)
        if date != now_date:
            db.update_date_test(callback.from_user.id, now_date)
            db.update_ball(callback.from_user.id, 10)
            msg = '\n\n<i>Тебе начислено 10 баллов за вариант</i>'
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        message = await bot.send_message(chat_id=callback.message.chat.id, text="Я выбираю лучший вариант для тебя\n<i>Секундочку...</i>")
        dictionary_subjects = {"math": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1},
                               "inf": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1},
                               "rus": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1},
                               "phys": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1},
                               "en": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 1, 37: 1, 38: 1, 39: 1, 40: 1, 41: 1, 42: 1},
                               "soc": {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1}}
        save_path, save_path_solutions = get_test(
            subject=str(subject), problems=dictionary_subjects[subject])
        documents = [InputMediaDocument(media=FSInputFile(path=str(save_path), filename="вариант.pdf")), InputMediaDocument(media=FSInputFile(
            path=str(save_path_solutions), filename="решение.pdf"))]
        await bot.send_media_group(chat_id=callback.message.chat.id, media=documents)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        try:
            os.remove(save_path)
            os.remove(save_path_solutions)
        except:
            pass
        await bot.send_message(chat_id=callback.message.chat.id, text="Ты большой молодец!"+msg, reply_markup=main_inline_keyboard())
        await state.clear()
    elif callback.data == "back_main":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Чем займёмся?", reply_markup=main_inline_keyboard())
        await state.clear()


async def choose_subject_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(FSMsubject.subject)
    await state.set_data({"subject": callback.data})
    list_words = ['Хороший выбор', 'Без проблем',
                  'Окей', 'Я люблю этот предмет', 'Смело']
    randint1 = randint(0, 4)
    msg = f"{list_words[randint1]}. Будем учить теорию или попрактикуемся?)"
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=msg, reply_markup=choose_type_inline_keyboard())


async def admin_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    if callback.data == "count_users":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f"<b>Количество пользователей:</b> {len(db.get_users_id())}", reply_markup=callback.message.reply_markup)
    elif callback.data == "DB":
        msg = ''
        for i in db.get_db_data():
            username = (await bot.get_chat_member(int(i[1]), int(i[1]))).user.username
            msg += f"{i[0]}. username: @{username} ball: {i[2]} act: {i[4]} {i[5]} task: {i[3]}\n"
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f"<b>База данных:</b>\n\n"+msg, reply_markup=callback.message.reply_markup)
    elif callback.data == "push_message":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Введите сообщение для отправки всем пользователям", reply_markup=admin_cancel_inline_keyboard())
        await state.set_state(FSMadmin.message_push)
    elif callback.data == "cancel":
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Отмена", reply_markup=admin_menu_inline_keyboard())
        await state.clear()
    elif callback.data == "send_db":
        file = FSInputFile(path='users.db', filename="users.db")
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Отправка базы данных", reply_markup=admin_menu_inline_keyboard())
        await bot.send_document(chat_id=callback.message.chat.id, document=file)
