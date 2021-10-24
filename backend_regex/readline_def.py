# -*- coding: utf-8 -*-

import re

row_no = 0
rejex_method_name = "def( |\t)+(\w+)( |\t)*\((.*)\)( |\t)*:"
rejex_method_name_back = "def( |\t)+(\w+)( |\t)*\((.*)\)( |\t)*->( |\t)*(\w+)( |\t)*:"

def make_args(lst):
  args = ''
  flag = False
  for s in lst:
    if s == '':
      continue
    if s == ',':
      flag = True
      args += s
    else:
      if flag:
        args += (' ' + s)
        flag = False
      else:
        args += s
  return args


fileobj = open("def_sample.py", "r", encoding="utf_8")
while True:
  line = fileobj.readline()
  if line:
    row_no += 1
    #for s in line:
    print(row_no, ":", line)
    # 1行づつ正規表現にかける(sub_paterns[0][1]に関数名が入っている。)

    # まず、戻り値パターン
    sub_paterns_back = re.findall(rejex_method_name_back, line)
    if sub_paterns_back:
      # 括弧の中の考慮
      lst = re.split('[\s]',(sub_paterns_back[0][3]))
      args = make_args(lst)
      str = "def " + sub_paterns_back[0][1] + "(" + args + ") -> "\
            + sub_paterns_back[0][6] + ":"
    else:
      sub_paterns = re.findall(rejex_method_name, line)
      # 括弧の中の考慮
      if not sub_paterns:
       	continue
      print(sub_paterns[0][3])
      lst = re.split('[\s]',(sub_paterns[0][3]))
      args = make_args(lst)
      
      str = "def " + sub_paterns[0][1] + "(" + args + "):"
    print(str)
  else:
    break
