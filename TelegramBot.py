import re
from datetime import timedelta
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from GoogleSheet import GoogleSheet
from NotionAPI import NotionAPI, show_to_do_list


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Xin chào, tôi là Echo <=3')


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')


class TelegramBot:
    def __init__(self, token: str, bot_username: str, sheet: GoogleSheet, notion_api: NotionAPI):
        self.TOKEN: Final = token
        self.BOT_USERNAME: Final = bot_username
        self.sheet = sheet
        self.notion_api = notion_api
        # self.gs = gspread.service_account(gs_credentials)
        # self.idSheet = idSheet
        self.app = Application.builder().token(self.TOKEN).build()

        # Command
        self.app.add_handler(CommandHandler('start', start_command))

        # Messages
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))

        # Error
        self.app.add_error_handler(error)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text = update.message

        print(f'User ({update.message.chat.id}) in {message_type}: "{text.text}"')

        response = self.handle_response(text)

        print('Bot:', response)
        await update.message.reply_text(response)

    def handle_response(self, text) -> str:
        content = text.text.lower()

        # Regex for income and expenses
        new_content = re.match(r'(.+?)\s(\d+)\s*(.+)?', content)

        # Regex for timekeeping to record a specific date (ex: 23/02 s)
        new_content_timekeeping = re.match(r'(\d{1,2}/\d{1,2})\s*([a-zA-Z]+)', content)
        new_date = text.date + timedelta(hours=7)
        new_date_str = new_date.strftime("%d/%m/%Y %H:%M:%S")

        self.notion_api.read_database()

        # add new income
        if content.startswith("t ") and new_content:
            return self.sheet.add_new_income(new_content, new_date_str)

        # add new exponse
        elif new_content and content[0] != '/':
            return self.sheet.add_new_exponse(new_content, new_date_str)

        # Timekeeping on a certain date
        # elif new_content_timekeeping:
        #     return self.sheet.add_new_timekeeping(new_content_timekeeping)

        # timekeepint during the day
        # elif content == 's' or content == 'c' or content == 'b':
        #     return self.sheet.timekeeping_during_the_day(content, new_date_str)

        # Get
        if content == "/c":
            return self.sheet.get_one_month_statistics(content)

        elif content == "/t":
            return self.sheet.get_one_month_statistics(content)

        # elif content == "/w":
        #     return self.sheet.get_one_month_statistics(content)

        elif content.startswith("/c "):
            return self.sheet.get_one_month_statistics(content)

        elif content.startswith("/t "):
            return self.sheet.get_one_month_statistics(content)

        # elif content.startswith("/w "):
        #     return self.sheet.get_one_month_statistics(content)

        elif str(content) == "/help":
            return ("🔊 Danh sách các lệnh:\n\n<thông tin> <giá tiền> <ghi chú> - Thêm vào danh sách chi\nt <thông "
                    "tin> <giá tiền> <ghi chú> - Thêm vào danh sách thu\n/c - Tổng chi tháng này\n/c <tháng> - Tổng "
                    "chi tháng truy vấn\n/t - Tổng thu tháng này\n/c <tháng> - Tổng thu tháng truy vấn\ns - Chấm công "
                    "buổi sáng\nc - Chấm công buổi chiều\nb - Chấm công cả ngày\n<ngày/tháng> <s, c, b> - chấm công "
                    "theo ngày\n/w - Thống kê đi làm tháng này\n/w <tháng> - Thống kê đi làm theo tháng truy vấn")

        # Notion API
        elif str(content) == "/d":
            # return show_to_do_list(self.notion_api.filter_todo_list("today"), "hôm nay")
            return show_to_do_list(self.notion_api.pages, "hôm nay")

        elif str(content) == "/w":
            return show_to_do_list(self.notion_api.filter_todo_list("week"), "tuần này")

        elif str(content) == "/m":
            return show_to_do_list(self.notion_api.filter_todo_list("month"), "tháng này")

        return 'Nói gì bố m đéo hiểu!!!'

    def run(self):
        print("Bắt đầu")
        self.app.run_polling(poll_interval=3)
