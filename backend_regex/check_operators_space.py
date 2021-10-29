import re

REJEX_METHOD_NAME = "def([ |\t]+)(\\w+)([ |\t]*)\\((.*)\\)([ |\t]*):"
REJEX_METHOD_NAME_BACK = "def([ |\t]+)(\\w+)([ |\t]*)\\((.*)\\)([ |\t]*)->([ |\t]*)(\\w+)([ |\t]*):"
REJEX_CLASS_NAME = "class([ |\t]*)(\\w+)([ |\t]*)(\\((.*)\\))*([ |\t]*):"

# 行ごとに実行 : 指定した演算子
def check_operators_space(line: str):
    if not (re.findall(REJEX_METHOD_NAME, line)
        or re.findall(REJEX_METHOD_NAME_BACK, line)
        or re.findall(REJEX_CLASS_NAME, line)):
        # スライス内の演算子の前後にはスペースを追加しない
        if(not re.findall('\\[.*:.*\\]', line)):
            line = re.sub(
                '([a-zA-Z0-9]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([a-zA-Z0-9]*)',
                '\\1 \\2 \\3',
                line)
            line = line.replace("  ", " ")
    return line

