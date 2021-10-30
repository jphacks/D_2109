import re

REJEX_METHOD_NAME = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*):"
REJEX_METHOD_NAME_BACK = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*)->([ |\t]*)(\w+)([ |\t]*):"
REJEX_CLASS_NAME = "class([ |\t]*)(\w+)([ |\t]*)(\((.*)\))*([ |\t]*):"

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

# 走査: 関数とクラスの整形
def scan_format_method_class(lst, op_format):
  def_blank_num = 0
  class_blank_num = 0

  if not op_format['action']:
    return {
      'lst': lst,
      'def-blank': def_blank_num,
      'class-blank': class_blank_num
    }
  lst_cp = []
  for row_no, line in enumerate(lst, 1):
    str_line = line

    # 先頭の空白文字を取得
    blank_str = re.match(r" *", line).end() * ' '

    # 1行づつ正規表現にかける

    # 関数: 戻り値パターン -> 通常パターン
    sub_paterns_back = re.findall(REJEX_METHOD_NAME_BACK, line)
    if sub_paterns_back:
      # 括弧の中の考慮
      ##printsub_paterns_back[0])
      for i, elem in enumerate(sub_paterns_back[0]):
        if (i == 0 or i == 4 or i == 5) and elem != ' ':
          def_blank_num += 1
        elif (i == 2 or i == 7) and elem != '':
          def_blank_num += 1
      args = make_args(sub_paterns_back[0][3])
      str_line = blank_str + "def " + sub_paterns_back[0][1] + "(" + args + ") -> "\
            + sub_paterns_back[0][6] + ":"
    else:
      sub_paterns = re.findall(REJEX_METHOD_NAME, line)
      # 括弧の中の考慮
      if sub_paterns:
        for i, elem in enumerate(sub_paterns[0]):
          if i == 0 and elem != ' ':
            def_blank_num += 1
          elif (i == 2 or i == 4) and elem != '':
            def_blank_num += 1
        args = make_args(sub_paterns[0][3])
        str_line = blank_str + "def " + sub_paterns[0][1] + "(" + args + "):"

    # class
    sub_paterns_class = re.findall(REJEX_CLASS_NAME, line)
    if sub_paterns_class:
      #print(sub_paterns_class[0])
      if not sub_paterns_class[0][3].startswith('('):
        # ()がないパターン
        for i, elem in enumerate(sub_paterns_class[0]):
          if i == 0 and elem != ' ':
            class_blank_num += 1
          elif i == 2 and elem != '':
            class_blank_num += 1
        str_line = blank_str + "class " + sub_paterns_class[0][1] + ":"
      else:
        for i, elem in enumerate(sub_paterns_class[0]):
          if i == 0 and elem != ' ':
            class_blank_num += 1
          elif (i == 2 or i == 5) and elem != '':
            class_blank_num += 1
        args = make_args(sub_paterns_class[0][4])
        str_line = blank_str + "class " + sub_paterns_class[0][1] + "(" + args + "):"
    lst_cp.append(str_line)
  #print(f"def-blank:{def_blank_num}箇所")
  #print(f"class-blank:{class_blank_num}箇所")
  return {
    'lst': lst_cp,
    'def-blank': def_blank_num,
    'class-blank': class_blank_num
  }