from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="1")
    kb.button(text="2")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def timekeeping() -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="Sáng", callback_data="morning"),
            types.InlineKeyboardButton(text="Chiều", callback_data="afternoon")
        ],
        [types.InlineKeyboardButton(text="Cả ngày", callback_data="both")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def statistical_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="Tổng chi tháng này", callback_data="callback_expense"),
            types.InlineKeyboardButton(text="Tổng thu tháng này", callback_data="callback_income"),
            types.InlineKeyboardButton(text="Bảng chấm công", callback_data="callback_timekeeping")
        ],
        [types.InlineKeyboardButton(text="Chọn tháng khác", callback_data="month_selection")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def todo_list_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="Hôm nay", callback_data="today_todo_list"),
            types.InlineKeyboardButton(text="Tuần này", callback_data="week_todo_list"),
            types.InlineKeyboardButton(text="Tháng này", callback_data="month_todo_list")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
