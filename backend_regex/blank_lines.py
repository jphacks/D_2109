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
head_blank_all = []
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
		head_blank_all.append(sub_pattern_all[0])
		print('head', head_blank_all) # debug
		# ブロックから出たか判定
		# if len(stack_blank.stack) != 0:  # スタック空の時にエラー出ないように
		# 	print(f"'{head_blank_all}'")
		# 	print(f"'{stack_blank.stack[-1]}'")
		# 	if len(head_blank_all) <= len(stack_blank.stack[-1]) or row_no == final_line:
		# 		print('exit block')
		# 		stack_blank.pop()
		# 		start_line = stack_start_line.pop()
		# 		if row_no == final_line:
		# 			end_line = row_no
		# 		else:
		# 			end_line = row_no - 1
		# 		# グローバル関数の場合
		# 		if len(stack_blank.stack) == 0: 
		# 			# blockの最初と最後の行番号をリストに保存
		# 			line_glob.append([start_line, end_line])
		# 		# 内部関数の場合
		# 		else:
		# 			line_menb.append([start_line, end_line])
		# 関数を含む行か判定
		if len(sub_pattern_def) != 0:
			print('enter def')
			# stack_blankに行頭の空白を保存
			stack_blank.push(sub_pattern_def[0][0])
			# ブロックの最初の行番号を保存
			stack_start_line.push(row_no)
			
	else:
		break

# print(len(stack_start_line.stack))
# print(len(stack_blank.stack))
# print(len(head_blank_all))
# sys.exit()

for idx_def, blank_def in enumerate(reversed(stack_blank.stack)):
	print("def", idx_def)
	print(f"blank_def: '{blank_def}'")
	print("len(blank_def)", len(blank_def))
	start_line = stack_start_line.pop()
	for idx_all, blank_all in enumerate(head_blank_all):
		# if idx_all + 1 <= stack_start_line.stack[-1]:
		# 関数より上の行は飛ばす
		if idx_all + 1 <= start_line:
			continue
		# ブロック抜けを判定
		if len(blank_all) <= len(blank_def):
			# グローバル関数の場合
			if len(blank_def) == 0: 
				# blockの最初と最後の行番号をリストに保存
				line_glob.append([start_line, idx_all])
			# 内部関数の場合
			else:
				line_menb.append([start_line, idx_all])
			break
		# 最後の関数が上の条件を満たさずに最後まで来た場合
		elif idx_all + 1 == len(head_blank_all):
			# グローバル関数の場合
			if len(blank_def) == 0:
				# blockの最初と最後の行番号をリストに保存
				line_glob.append([start_line, idx_all + 1])
			# 内部関数の場合
			else:
				line_menb.append([start_line, idx_all + 1])
			break





print(line_menb)
print(line_glob)