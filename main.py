import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import questions


async def main():
    load_dotenv()
    token = os.getenv("token")
    bot = Bot(token=token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(questions.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    load_dotenv()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

    os.remove("credentials.json")
    os.remove("courses_database.json")
    os.remove("to_do_list_database.json")
