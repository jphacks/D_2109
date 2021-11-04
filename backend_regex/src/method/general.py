import re

# 行頭の空白文字列を取得
def get_start_blank(line: str) -> str:
    starts_blank = re.match(r" *", line).end() * ' '
    return starts_blank


# 行頭の空白文字列数を取得
def get_start_blank_num(line: str) -> int:
    return re.match(r" *", line).end()


# 空行をきれいにする
def strip_blank_line(code_lst: list) -> list:
  return list(map(lambda x: x.strip() if x.strip() == '' else x, code_lst))


# コード配列の各要素の行末に改行文字
def add_newline_char(code_lst: list) -> list:
  return list(map(lambda x: x + '\n' if not x.endswith('\n') else x , code_lst))


# 括弧の中を整形
def make_args(s_lst):
  s_lst = re.sub('[\s]', '', s_lst)
  lst = re.split(',', s_lst)
  args = ''
  for i, s in enumerate(lst):
    if i == 0:
      args += s
      continue
    args += ', ' + s
  return args
