import re

from cls.stack import InitDisplayStack
from method.general import get_start_blank_num


# 走査して、適切なインデントに調節していく
def scan_indent_config(lst_cp: list, op_indent: dict) -> list:
  stack_indent = InitDisplayStack(0)
  stack = InitDisplayStack(0)
  INDENT_NUM = op_indent['tab_num'] if op_indent['type'] == '\t' else op_indent['num']

  bef = 0
  lst_after = []
  for row_no, line in enumerate(lst_cp, 1):
      str_line = line
      # もし空行ならindentをstack_indentのheadに合わせる
      if re.match(r"$ *^", str_line):
          str_line = stack_indent.get_top() * ' '
      aft = get_start_blank_num(str_line)
      
      # コメント行は無視
      if str_line.startswith("#"):
          lst_after.append(str_line)
          continue
      if bef > aft:
        for i, elem in enumerate(stack.get_reverse_lst()):
            if elem == aft:
                # この時のiがpop数
                for j in range(i):
                    stack_indent.pop()
                    stack.pop()
      head = stack_indent.get_top()
      if aft != head:
          blank = head * ' '
          # 適切な行頭空白文字を付加
          str_line = blank+str_line.strip()
      
      if str_line.endswith(':'):
          stack_indent.push(head + INDENT_NUM)
          # 1つ先読み
          try:
            stack.push(get_start_blank_num(lst_cp[row_no]))
          except Exception:
            pass
      lst_after.append(str_line)
      bef = aft
  return lst_after