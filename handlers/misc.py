from aiogram import html
import re


def check_regex_expense(text) -> bool:
    regex_pattern = re.fullmatch(r'(.+?)\s(\d+)\s*(.+)?', text)
    if regex_pattern:
        return True
    return False


def check_regex_timekeeping(text) -> bool:
    regex_pattern = re.fullmatch(r'(\d{1,2}/\d{1,2})\s*([a-zA-Z]+)', text)
    if regex_pattern:
        return True
    return False


