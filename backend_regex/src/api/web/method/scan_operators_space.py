import re

from method.naming import MethodNaming, ClassNaming
from method.general import make_args
from constants import REJEX_METHOD_NAME, REJEX_METHOD_NAME_BACK, REJEX_CLASS_NAME


# 前後の空白を調整(1行分)
def check_operators_space(line: str, method_naming: MethodNaming, class_naming: ClassNaming) -> str:
    #print(f"met:{method_naming.method_lst}")
    #print(class_naming.class_lst)
    strip_str = line.strip()
    # コメント行や空文字のみの行はpass
    if strip_str.startswith('#') or strip_str == '':
      return line

    if not (re.findall(REJEX_METHOD_NAME, line)
        or re.findall(REJEX_METHOD_NAME_BACK, line)
        or re.findall(REJEX_CLASS_NAME, line)):
        #REJEX = (f'(\([^)]*\))')
        #remove_str_line = re.sub(REJEX_STRING_SINGLE_STRICT + '|' + REJEX_STRING_DOUBLE_STRICT + '|' + REJEX_COMMENT, '', line)
        
        for s in list(set(method_naming.method_lst)):
          REJEX = (f'{s}\s*\(.+\)')
          if re.findall(REJEX, line):
            args = make_args(re.findall(REJEX, line)[0])
            strip_str = re.sub(f'{s}\s*\(.+\)', args, strip_str)

        for s in list(set(class_naming.class_lst)):
          REJEX = (f'{s}\s*\(.+\)')
          if re.findall(REJEX, line):
            args = make_args(re.findall(REJEX, line)[0])
            strip_str = re.sub(f'{s}\s*\(.+\)', args, strip_str)

        # 行のword内に' 'が2つ以上入っていたら' '1つにする
        strip_str_lst = [s for s in re.split('\s', strip_str) if s != '']
        #print(strip_str_lst)
        n = len(strip_str_lst)
        #print(n)
        #REJEX = "([\w=]+( {2,}))" * n
        # 行頭のインデントを取得
        s = re.match(r" *", line).end() * ' '
        for i, st in enumerate(strip_str_lst):
          if i != len(strip_str_lst):
            s += st + ' '
          else:
            s += st
        line = s
        #print("###########")
        #print(line)

        # スライス内の演算子の前後にはスペースを追加しない
        if(not re.findall('\\[.*:.*\\]', line)):
            if(not re.findall('([a-zA-Z0-9]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([a-zA-Z0-9]*)',line)):
                line = re.sub(
                    '([a-zA-Z0-9]*)([\s]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([\s]*)([a-zA-Z0-9]*)',
                    '\\1 \\3 \\5',
                    line)
        # lineの末尾を確認

    return line


# 前後の空白を調整(走査)
def scan_operators_space(lst: list, method_naming, class_naming) -> list:
  lst_cp = []
  for line in lst:
    lst_cp.append(check_operators_space(line, method_naming, class_naming))
  return lst_cp