import re

# スタックの定義
class MyStack_Indent:
    def __init__(self, n):
        self.stack = [0]
    def get_top(self):
      return self.stack[-1]
    def get_reverse_lst(self):
        return reversed(self.stack)
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        result = self.stack[-1]  # 末尾の要素を変数に取り出す
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する


# 走査して、適切なインデントに調節していく
def scan_indent_config(lst_cp, op_indent):
  stack_indent = MyStack_Indent(0)
  stack = MyStack_Indent(0)
  INDENT_NUM = op_indent['tab_num'] if op_indent['type'] == '\t' else op_indent['num']

  bef = 0
  lst_after = []
  for row_no, line in enumerate(lst_cp, 1):
      str_line = line
      # もし空行ならindentをstack_indentのheadに合わせる
      if re.match(r"$ *^", str_line):
          str_line = stack_indent.get_top() * ' '
      aft = re.match(r" *", str_line).end()
      
      
      #print(f"bef: {bef}")
      #print(f"aft: {aft}")
      
      # コメント行は無視
      if str_line.startswith("#"):
          lst_after.append(str_line)
          continue
      if bef > aft:
        for i, elem in enumerate(stack.get_reverse_lst()):
            #print(elem)
            if elem == aft:
                #print(f"pop数: {i}")
                # この時のiがpop数
                for j in range(i):
                    stack_indent.pop()
                    #print(f"pop: {stack_indent.pop()}")
                    stack.pop()
      head = stack_indent.get_top()
      if aft != head:
          #print(f"head: {head}")
          blank = head * ' '
          # 適切な行頭空白文字を付加
          str_line = blank+str_line.strip()
      
      if str_line.endswith(':'):
          #print(f"先読み:{str_line}")
          #printlst_cp[row_no])
          stack_indent.push(head + INDENT_NUM)
          # 1つ先読み
          try:
            stack.push(re.match(r" *", lst_cp[row_no]).end())
          except Exception:
            pass
      ##printstack_indent.stack)
      ##printstack.stack)
      lst_after.append(str_line)
      bef = aft
  ##printlst_after)
  return lst_after