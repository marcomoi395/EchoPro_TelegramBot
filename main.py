import os
from dotenv import load_dotenv
from GoogleSheet import GoogleSheet
from NotionAPI import NotionAPI, get_name_course_by_id, show_to_do_list, filter_todo_list
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
        to_do_list_database_id=os.getenv("to_do_list_database_id"),
        courses_database_id=os.getenv("courses_database_id")
    )

    notion_api.read_courses_database()
    notion_api.read_to_do_list_database()
    #
    # print(show_to_do_list(filter_todo_list("month"), "tháng này"))
    # print(get_name_course_by_id("9b215009-dac0-40b2-b9fe-8ef2ea4133b8"))

    bot = TelegramBot(
        token=os.getenv("token"),
        bot_username=os.getenv("bot_username"),
        sheet=sheet,
        notion_api=notion_api
    )

    bot.run()
    os.remove(file_path)
    os.remove("courses_database.json")
    os.remove("to_do_list_database.json")
