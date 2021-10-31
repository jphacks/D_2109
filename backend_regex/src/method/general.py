import re

# 行頭の空白文字列を取得
def get_start_blank_num(line: str) -> str:
    starts_blank = re.match(r" *", line).end() * ' '
    return starts_blank