import os
import re
from datetime import timedelta

from aiogram import Router, F, html
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from dotenv import load_dotenv

from API.GoogleSheet import GoogleSheet
from API.NotionAPI import show_to_do_list, filter_todo_list
from handlers.misc import check_regex_expense, check_regex_timekeeping
from keyboards.for_questions import get_yes_no_kb, timekeeping, statistical_keyboard, \
    todo_list_keyboard, show_list_month, statistical_for_another_month_keyboard, undo_keyboard

load_dotenv()

# create credentials.json for googlesheet
gs_credentials = os.getenv("gs_credentials")
file_path = "credentials.json"
with open(file_path, "w") as file:
    file.write(gs_credentials)

sheet = GoogleSheet(
    gs_credentials="credentials.json",
    idSheet=os.getenv("sheet")
)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Thanh Loi không cần bot, bot cần Thanh Loi",
        reply_markup=get_yes_no_kb()
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(f"Hello, hỏi {html.bold("Thanh Loi")}!")


# Timekeeping
@router.message(Command("check"))
async def check_timekeeping(message: Message):
    await message.answer(
        "🤡 Chọn cho chính xác vào!!!\n\n",
        reply_markup=timekeeping()
    )


@router.message(Command("undo"))
async def undo_command(message: Message):
    await message.answer(
        "🤡 Chọn mục bạn muốn hoàn tác",
        reply_markup=undo_keyboard()
    )


# statistical
@router.message(Command("s"))
async def statistical(message: Message):
    await message.answer(
        "📌 Thống kê tháng này\n\n",
        reply_markup=statistical_keyboard()
    )


# todo_list
@router.message(Command("t"))
async def show_todo_list(message: Message):
    await message.answer(
        "📌 Danh sách công việc theo\n\n",
        reply_markup=todo_list_keyboard()
    )


# Đúng/Sai
@router.message(F.text == "Đúng")
async def yes(message: Message):
    await message.answer("Chắc chắn là như thế rồi!!!", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Sai")
async def no(message: Message):
    await message.answer("Mấy con gà biết gì:)", reply_markup=ReplyKeyboardRemove())


# Timekeeping
@router.message(F.text == "Sáng")
async def with_puree(message: Message):
    new_date = message.date + timedelta(hours=7)
    new_date_str = new_date.strftime("%d/%m/%Y %H:%M:%S")
    await message.answer(sheet.timekeeping_during_the_day(message.text, new_date_str),
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Chiều")
async def with_puree(message: Message):
    new_date = message.date + timedelta(hours=7)
    new_date_str = new_date.strftime("%d/%m/%Y %H:%M:%S")
    await message.answer(sheet.timekeeping_during_the_day(message.text, new_date_str),
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Cả ngày")
async def with_puree(message: Message):
    new_date = message.date + timedelta(hours=7)
    new_date_str = new_date.strftime("%d/%m/%Y %H:%M:%S")
    await message.answer(sheet.timekeeping_during_the_day(message.text, new_date_str),
                         reply_markup=ReplyKeyboardRemove())


# income and expense
@router.message(F.text)
async def income_and_expense(message: Message):
    if check_regex_expense(message.text.lower()):
        if message.text.lower().startswith("t "):
            new_content = re.match(r'(.+?)\s(\d+)\s*(.+)?', message.text)
            new_date = message.date + timedelta(hours=7)
            new_date_str = new_date.strftime("%d/%m/%Y %H:%M:%S")
            await message.answer(
                sheet.add_new_income(new_content, new_date_str),
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            content = message.text
            new_content = re.match(r'(.+?)\s(\d+)\s*(.+)?', content)
            new_date = message.date + timedelta(hours=7)
            new_date_str = new_date.strftime("%d/%m/%Y %H:%M:%S")
            await message.answer(
                sheet.add_new_exponse(new_content, new_date_str),
                reply_markup=ReplyKeyboardRemove()
            )
    elif check_regex_timekeeping(message.text.lower()):
        new_content = re.match(r'(\d{1,2}/\d{1,2})\s*([a-zA-Z]+)', message.text)
        await message.answer(
            sheet.add_new_timekeeping(new_content),
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Bố mày éo hiểu!!!",
            reply_markup=ReplyKeyboardRemove()
        )


# Callback Query To-do List
@router.callback_query(F.data == "today_todo_list")
async def send_today_todo_list(callback: CallbackQuery):
    await callback.message.answer(show_to_do_list(filter_todo_list("today"), "hôm nay"))


@router.callback_query(F.data == "week_todo_list")
async def send_week_todo_list(callback: CallbackQuery):
    await callback.message.answer(show_to_do_list(filter_todo_list("week"), "tuần này"))


@router.callback_query(F.data == "month_todo_list")
async def send_month_todo_list(callback: CallbackQuery):
    await callback.message.answer(show_to_do_list(filter_todo_list("month"), "tháng này"))


# Callback Query Undo
@router.callback_query(F.data.startswith("callback_undo"))
async def undo_callback(callback: CallbackQuery):
    name = callback.data.split()[1]
    if name == "expense":
        number_sheet = 0
    elif name == "income":
        number_sheet = 1
    else:
        number_sheet = 2
    await callback.message.answer(sheet.undo_income(number_sheet))


# Callback Query Statistical
@router.callback_query(F.data.startswith("callback_expense"))
async def expense_statistical(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer(sheet.get_one_month_statistics(f"/c {month}"))


@router.callback_query(F.data.startswith("callback_income"))
async def income_statistical(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer(sheet.get_one_month_statistics(f"/t {month}"))


@router.callback_query(F.data.startswith("callback_timekeeping"))
async def timekeeping_statistical(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer(sheet.get_one_month_statistics(f"/w {month}"))


@router.callback_query(F.data == "month_selection")
async def month_selection(callback: CallbackQuery):
    await callback.message.answer("📌 Chọn tháng muốn thông kê\n\n", reply_markup=show_list_month())


@router.callback_query(F.data.startswith("Tháng "))
async def list_month(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer("📌 Chọn mục thống kê\n\n", reply_markup=statistical_for_another_month_keyboard(month))
