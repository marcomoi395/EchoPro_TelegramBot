import re


def check_regex_expense(text) -> bool:
    regex_pattern = re.fullmatch(r'(.+?)\s(\d+)\s*(.+)?', text)
    if regex_pattern:
        return True
    return False
