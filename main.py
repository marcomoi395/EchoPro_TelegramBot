import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from API.NotionAPI import NotionAPI
from handlers import questions, different_types


async def main():
    load_dotenv()

    # create credentials.json for googlesheet
    gs_credentials = os.getenv("gs_credentials")
    file_path = "credentials.json"
    with open(file_path, "w") as file:
        file.write(gs_credentials)

    bot = Bot(token="6961709005:AAG-OPYRAe3VSblLmJVbB1X6C6GhUUMqkbk",
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(questions.router, different_types.router)

    # Connect with Notion
    notion_api = NotionAPI(
        token=os.getenv("notion_token"),
        to_do_list_database_id=os.getenv("to_do_list_database_id"),
        courses_database_id=os.getenv("courses_database_id")
    )

    # Read database
    notion_api.read_courses_database()
    notion_api.read_to_do_list_database()

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
