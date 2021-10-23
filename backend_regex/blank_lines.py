# -*- coding: utf-8 -*-

import re
import sys

# スタックの定義
class MyStack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        result = self.stack[-1]  # 末尾の要素を変数に取り出す
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する

stack_blank = MyStack()
stack_start_line = MyStack()
line_glob = []
line_menb = []
row_no = 0
rejex_method_name = "(^[ \t]*)def[ \t]+(\w+)[ \t]*\(.*\)[ \t]*:"
all_line_re = "^[ \t]*"
fileobj = open("def_sample.py", "r", encoding="utf_8")
final_line = sum([1 for _ in open('def_sample.py')])
print(final_line)
while True:
	line = fileobj.readline()
	if line:
		row_no += 1
		print(row_no, ":", line)
		# 関数の判定
		sub_pattern_def = re.findall(rejex_method_name, line)
		print("def", sub_pattern_def)
		# 行頭のスペース・タブを抽出
		sub_pattern_all = re.findall(all_line_re, line)
		print('all', sub_pattern_all)
		# sys.exit()
		head_blank_all = sub_pattern_all[0]
		print('head', head_blank_all) # debug
		# ブロックから出たか判定
		if len(stack_blank.stack) != 0:  # スタック空の時にエラー出ないように
			print('here')
			if head_blank_all == stack_blank.stack[-1] or row_no == final_line:
				print('exit block')
				stack_blank.pop()
				start_line = stack_start_line.pop()
				if row_no == final_line:
					end_line = row_no
				else:
					end_line = row_no - 1
				# グローバル関数の場合
				if len(stack_blank.stack) == 0: 
					# blockの最初と最後の行番号をリストに保存
					line_glob.append([start_line, end_line])
				# 内部関数の場合
				else:
					line_menb.append([start_line, end_line])
		# 関数を含む行か判定
		if len(sub_pattern_def) != 0:
			print('enter def')
			# stack_blankに行頭の空白を保存
			stack_blank.push(sub_pattern_def[0][0])
			# ブロックの最初の行番号を保存
			stack_start_line.push(row_no)

		# # blockから抜けた時(直後が関数でもそれ以外でも可)
		# if in_block == True and len(sub_pattern) == 0:

		# 	in_block == False
		# # blockに入る時
		# elif len(sub_pattern) != 0:

		# 	in_block = True
		# 	bf_def = sub_pattern[0][0]
		# 	print(f"sub_pattern[0]: '{bf_def}'")
	else:
		break

print(line_menb)
print(line_glob)

# スタッククラスの定義
# class MyStack:
#     def __init__(self):
#         self.stack = []
#     def push(self, item):
#         self.stack.append(item)
#     def pop(self):
#         result = self.stack[-1]  # 末尾の要素を変数に取り出す
#         del self.stack[-1]  # リストから要素を削除する
#         return result  # リスト末尾から取り出したデータを返送する

# while ファイル終わるまで
# 	if stack != 空
# 		if 頭の空白 == stack[top]
# 			stack.pop
# 			if stack == 空(=グローバル)
# 				last_line_glob.append(行数)
# 			else(=クラスor関数内)
# 				last_line_menb.append(行数)
	
# 	if defかclassを発見
# 		if stack == 空(=グローバル)
# 			start_line_glob.append(行数)
# 		else(=クラスor関数内)
# 			start_line_menb.append(行数)
# 		stack.push(頭の空白)