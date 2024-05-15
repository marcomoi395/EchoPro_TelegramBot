from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="1")
    kb.button(text="2")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def timekeeping() -> ReplyKeyboardMarkup:
    buttons = [
        [
            types.KeyboardButton(text="Sáng"),
            types.KeyboardButton(text="Chiều")
        ],
        [types.KeyboardButton(text="Cả ngày")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Chọn cho đúng vào!!!"
    )
    return keyboard


def statistical_keyboard() -> InlineKeyboardMarkup:
    cur_month = datetime.now().month
    buttons = [
        [
            types.InlineKeyboardButton(text="Tổng chi", callback_data=f"callback_expense {cur_month}"),
            types.InlineKeyboardButton(text="Tổng thu", callback_data=f"callback_income {cur_month}"),
            types.InlineKeyboardButton(text="Bảng chấm công", callback_data=f"callback_timekeeping {cur_month}")
        ],
        [types.InlineKeyboardButton(text="Chọn tháng khác", callback_data="month_selection")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def statistical_for_another_month_keyboard(month) -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="Tổng chi", callback_data=f"callback_expense {month}"),
            types.InlineKeyboardButton(text="Tổng thu", callback_data=f"callback_income {month}"),
            types.InlineKeyboardButton(text="Bảng chấm công", callback_data=f"callback_timekeeping {month}")
        ]
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


def show_list_month() -> InlineKeyboardMarkup:
    cur_month = datetime.now().month
    builder = InlineKeyboardBuilder()
    for i in range(1, cur_month + 1):
        builder.button(text=f"Tháng {i}", callback_data=f"Tháng {i}")
    builder.adjust(cur_month)
    return builder.as_markup()
