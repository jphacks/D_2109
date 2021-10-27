# 行ごとに実行 : 指定した演算子
def check_operators_space(line: str):
    line = re.sub(
        '([a-zA-Z0-9]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([a-zA-Z0-9]*)',
        '\\1\\2\\3',
        line)
    line = line.replace("  ", " ")
    return line
