import os
from dotenv import load_dotenv
from GoogleSheet import GoogleSheet
from NotionAPI import NotionAPI
from TelegramBot import TelegramBot

if __name__ == '__main__':
    load_dotenv()
    gs_credentials = os.getenv("gs_credentials")
    file_path = "credentials.json"
    with open(file_path, "w") as file:
        file.write(gs_credentials)

    sheet = GoogleSheet(
        gs_credentials="credentials.json",
        idSheet=os.getenv("sheet")
    )

    notion_api = NotionAPI(
        token=os.getenv("notion_token"),
        database_id=os.getenv("database_id")
    )

    bot = TelegramBot(
        token=os.getenv("token"),
        bot_username=os.getenv("bot_username"),
        sheet=sheet,
        notion_api=notion_api
    )
    bot.run()
    os.remove(file_path)
    os.remove("db.json")
