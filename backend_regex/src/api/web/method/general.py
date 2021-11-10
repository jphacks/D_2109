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


# 末尾空白文字の削除
def delete_blank_ends(code_lst: list) -> list:
  return list(map(lambda x: x.rstrip(), code_lst))


# タブ文字を' '*INDENT_TAB_NUMに置き換え
def replace_tab_to_blank(code_lst: list, tab_nam: int) -> list:
  return list(map(lambda x: re.sub('\t', ' '*tab_nam, x), code_lst))


# インデント設定によってはタブ文字に戻す
def replace_blank_to_tab(code_lst: list, indent_char_type: str, indent_blank_num: int) -> list:
  if indent_char_type == '\t':
    return list(map(lambda x: re.sub(' '*indent_blank_num, '\t', x), code_lst))
  else:
    return code_lst


# インデント文字を取得
def get_indent(indent_char_type: str, indent_blank_num: int) -> str:
  return '\t' if indent_char_type == '\t' else ' '*indent_blank_num


# コード配列の各要素の行末に改行文字
def add_newline_char(code_lst: list) -> list:
  return list(map(lambda x: x + '\n' if not x.endswith('\n') else x , code_lst))


# 括弧の中を整形
def make_args(s_lst: str) -> str:
  s_lst = re.sub('[\s]', '', s_lst)
  lst = re.split(',', s_lst)
  args = ''
  for i, s in enumerate(lst):
    if i == 0:
      args += s
      continue
    args += ', ' + s
  return args
