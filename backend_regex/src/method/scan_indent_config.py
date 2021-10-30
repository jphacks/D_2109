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

# indent設定に合わせて\t=>' '*X文字にする
def scan_indent_config(lst, op_indent):
  INDENT_TAB_NUM = op_indent['tab_num']
  if op_indent['type'] == '\t':
    INDENT_NUM = op_indent['tab_num']
  else:
    INDENT_NUM = op_indent['num']
  
  # 末尾文字の削除
  lst_cp = list(map(lambda x: x.rstrip(), lst))

  # タブ文字を' '*INDENT_TAB_NUMに置き換え
  lst_cp = list(map(lambda x: re.sub('\t', ' '*INDENT_TAB_NUM, x), lst_cp))
  
  stack_indent = MyStack_Indent(0)
  stack = MyStack_Indent(0)

  bef = 0
  lst_after = []
  for row_no, line in enumerate(lst_cp, 1):
      #print(line)
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