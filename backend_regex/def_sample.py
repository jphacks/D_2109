# -*- coding: utf-8 -*-

import re

row_no = 0
rejex_method_name = "def[ |\t]+(\w+)[ |\t]*\(.*\)[ |\t]*:"

fileobj = open("a.py", "r", encoding="utf_8")
while True:
  line = fileobj.readline()
  if line:
    row_no += 1
    #for s in line:
    print(row_no, ":", line)
    sub_patern = re.findall(rejex_method_name, line)
    print(sub_patern)
  else:
    break