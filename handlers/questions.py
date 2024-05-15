from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_questions import get_yes_no_kb, timekeeping, statistical_keyboard, \
    todo_list_keyboard
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
        "Thống kê....",
        reply_markup=statistical_keyboard()
    )


@router.message(Command("t"))
async def statistical(message: Message):
    await message.answer(
        "Danh sách công việc theo",
        reply_markup=todo_list_keyboard()
    )


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
