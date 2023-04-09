from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from app.db.handlers import data_handler

router = Router()


@router.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer(f"Hi, {message.from_user.first_name}!")


@router.message()
async def json_handler(message: Message, dt_from=None, dt_upto=None, group_type=None, error=None):
    if error:
        await message.answer(error)
    elif group_type:
        dt_from = datetime.fromisoformat(dt_from)
        dt_upto = datetime.fromisoformat(dt_upto)
        msg = await data_handler(dt_from, dt_upto, group_type)
        await message.answer(msg)
    else:
        err = 'Невалидный запос. Пример запроса: \n' \
              '{"dt_from": "2022-09-01T00:00:00", "dt_upto": \n' \
              '"2022-12-31T23:59:00", "group_type": "month"}'
        await message.answer(err)

