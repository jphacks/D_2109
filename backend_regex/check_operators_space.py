import re

REJEX_METHOD_NAME = "def([ |\t]+)(\\w+)([ |\t]*)\\((.*)\\)([ |\t]*):"
REJEX_METHOD_NAME_BACK = "def([ |\t]+)(\\w+)([ |\t]*)\\((.*)\\)([ |\t]*)->([ |\t]*)(\\w+)([ |\t]*):"
REJEX_CLASS_NAME = "class([ |\t]*)(\\w+)([ |\t]*)(\\((.*)\\))*([ |\t]*):"

# 行ごとに実行 : 指定した演算子


def check_operators_space(line: str, mod_ope_num: int):
    if not (re.findall(REJEX_METHOD_NAME, line)
        or re.findall(REJEX_METHOD_NAME_BACK, line)
        or re.findall(REJEX_CLASS_NAME, line)):
        # スライス内の演算子の前後にはスペースを追加しない
        if(not re.findall('\\[.*:.*\\]', line)):
            if(not re.findall('([a-zA-Z0-9]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([a-zA-Z0-9]*)',line)):
                line = re.sub(
                    '([a-zA-Z0-9]*)([\s]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([\s]*)([a-zA-Z0-9]*)',
                    '\\1 \\3 \\5',
                    line)
                mod_ope_num = mud_ope_num + 1
    return line, mod_ope_num

