from datetime import datetime

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from API.NotionAPI import NotionAPI, filter_todo_list


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Đúng")
    kb.button(text="Sai")
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


def undo_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="Chi", callback_data="callback_undo expense"),
            types.InlineKeyboardButton(text="Thu", callback_data="callback_undo income"),
            types.InlineKeyboardButton(text="Chấm công", callback_data="callback_undo timekeeping")
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


# delete_keyboard
def delete_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            types.InlineKeyboardButton(text="Hôm nay", callback_data="delete today"),
            types.InlineKeyboardButton(text="Tuần này", callback_data="delete week"),
            types.InlineKeyboardButton(text="Tháng này", callback_data="delete month")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def show_todo_list_to_delete(filter_type) -> InlineKeyboardMarkup:
    pages = filter_todo_list(filter_type)
    builder = InlineKeyboardBuilder()
    for page in pages:
        if page:
            name = page["properties"]["Name"]["title"][0]["text"]["content"]
            record_id = page["id"]
            builder.button(text=f"{name}", callback_data=f"delete_with_id {record_id}")
    builder.adjust(1)
    return builder.as_markup()
