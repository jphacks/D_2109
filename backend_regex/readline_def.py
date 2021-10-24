# -*- coding: utf-8 -*-

import re

row_no = 0
rejex_method_name = "def( |\t)+(\w+)( |\t)*\((.*)\)( |\t)*:"
rejex_method_name_back = "def( |\t)+(\w+)( |\t)*\((.*)\)( |\t)*->( |\t)*(\w+)( |\t)*:"
rejex_class_name = "class( |\t)+(\w+)( |\t)*(\((.*)\))*( |\t)*:"

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


fileobj = open("def_sample.py", "r", encoding="utf_8")
while True:
  line = fileobj.readline()
  if line:
    row_no += 1
    #for s in line:
    #print(row_no, ":", line)
    str = line
    # 1行づつ正規表現にかける

    # 関数: 戻り値パターン -> 通常パターン
    sub_paterns_back = re.findall(rejex_method_name_back, line)
    if sub_paterns_back:
      # 括弧の中の考慮
      args = make_args(sub_paterns_back[0][3])
      str = "def " + sub_paterns_back[0][1] + "(" + args + ") -> "\
            + sub_paterns_back[0][6] + ":"
    else:
      sub_paterns = re.findall(rejex_method_name, line)
      # 括弧の中の考慮
      if sub_paterns:
        args = make_args(sub_paterns[0][3])
        str = "def " + sub_paterns[0][1] + "(" + args + "):"

    # class
    sub_paterns_class = re.findall(rejex_class_name, line)
    if sub_paterns_class:
      #print(sub_paterns_class[0])
      if not sub_paterns_class[0][3].startswith('('):
        # ()がないパターン
        str = "class " + sub_paterns_class[0][1] + ":"
      else:
        args = make_args(sub_paterns_class[0][4])
        str = "class " + sub_paterns_class[0][1] + "(" + args + "):"

    print(row_no, ":", str)
    
  else:
    break
