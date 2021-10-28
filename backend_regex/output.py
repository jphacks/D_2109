# -*- coding: utf-8 -*-
import re
import sys
import numpy as np
import pprint

FILE_PATH = "blank_lines.py"
SENTINEL = 1000000





# スタックの定義
class MyStack:






    def __init__(self):
        self.stack = []


    def push(self, item):
        self.stack.append(item)
    # コメント
    def pop(self):
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する