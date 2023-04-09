import logging
from aiogram import Bot, Dispatcher, F
from app.bot.middlewares import JsonMessageMiddleware
from app.bot.routers import router
from app.config.config import config

API_TOKEN = config["telegram"]['token']

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    router.message.filter(F.chat.type == "private")
    router.message.middleware(JsonMessageMiddleware())

    dp.include_router(router)
    await dp.start_polling(bot)



