from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from API.NotionAPI import show_to_do_list, filter_todo_list
from keyboards.for_questions import get_yes_no_kb, timekeeping, statistical_keyboard, \
    todo_list_keyboard, show_list_month, statistical_for_another_month_keyboard
from handlers.regex import check_regex_expense

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Вы довольны своей работой?",
        reply_markup=get_yes_no_kb()
    )


# Timekeeping
@router.message(Command("check"))
async def check_timekeeping(message: Message):
    await message.answer(
        "Chọn cho chính xác vào!!!",
        reply_markup=timekeeping()
    )


# statistical
@router.message(Command("s"))
async def statistical(message: Message):
    await message.answer(
        "Thống kê tháng này\n\n",
        reply_markup=statistical_keyboard()
    )


# todo_list
@router.message(Command("t"))
async def statistical(message: Message):
    await message.answer(
        "Danh sách công việc theo",
        reply_markup=todo_list_keyboard()
    )


# Timekeeping
@router.message(F.text == "Sáng")
async def with_puree(message: Message):
    await message.answer("1", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Chiều")
async def without_puree(message: Message):
    await message.answer("2", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Cả ngày")
async def without_puree(message: Message):
    await message.answer("3", reply_markup=ReplyKeyboardRemove())


# income and expense
@router.message(F.text)
async def income_and_expense(message: Message):
    if check_regex_expense(message.text.lower()):
        if message.text.lower().startswith("t "):
            await message.answer(
                "thu",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                "Chi!",
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


# Callback Query Statistical
@router.callback_query(F.data.startswith("callback_expense"))
async def expense_statistical(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer("callback_expense " + f"{month}")


@router.callback_query(F.data.startswith("callback_income"))
async def income_statistical(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer("callback_income " + f"{month}")


@router.callback_query(F.data.startswith("callback_timekeeping"))
async def timekeeping_statistical(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer("callback_timekeeping " + f"{month}")


@router.callback_query(F.data == "month_selection")
async def month_selection(callback: CallbackQuery):
    await callback.message.answer("month_selection", reply_markup=show_list_month())


@router.callback_query(F.data.startswith("Tháng "))
async def list_month(callback: CallbackQuery):
    month = callback.data.split()[1]
    await callback.message.answer("Chọn mục thống kê\n\n", reply_markup=statistical_for_another_month_keyboard(month))
