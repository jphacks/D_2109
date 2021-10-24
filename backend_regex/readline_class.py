# -*- coding: utf-8 -*-

import re

row_no = 0
rejex_class_name = "def( |\t)+(\w+)( |\t)*\((.*)\)( |\t)*:"

fileobj = open("def_sample.py", "r", encoding="utf_8")
while True:
  line = fileobj.readline()
  if line:
    row_no += 1
    #for s in line:
    #print(row_no, ":", line)
    # 1行づつ正規表現にかける(sub_paterns[1]に関数名が入っている。)
    sub_paterns = re.findall(rejex_class_name, line)
    #print(sub_paterns)
    if not sub_paterns:
    	continue
    # defの所を整形(flagは整形flag)
    flag = False
    if sub_paterns[0][0] == '\t':
      flag = True
    if sub_paterns[0][2] == ' ' or sub_paterns[0][2] == '\t':
      flag = True
    if (sub_paterns[0][4] == ' ') or (sub_paterns[0][4] == '\t'):
   		flag = True
    
    if flag:
      print(row_no)
      str = "def " + sub_paterns[0][1] + "(" + sub_paterns[0][3] + "):"
      print(str)
  else:
    break