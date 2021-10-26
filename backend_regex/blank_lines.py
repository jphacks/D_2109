# -*- coding: utf-8 -*-
import re
import sys
import numpy as np

FILE_PATH = "def_sample.py"

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

### defブロックのサーチ ### 
stack_blank = MyStack()
stack_start_line = MyStack()
line_glob = []
line_local = []
row_no = 0
rejex_method_name = "(^[ \t]*)def[ \t]+(\w+)[ \t]*\(.*\)[ \t]*:"
all_line_re = "(^[ \t\n]*)"
# blank_line_re = "[ \t]*\n"
fileobj = open(FILE_PATH, "r", encoding="utf_8")
final_line = sum([1 for _ in open('def_sample.py')])
head_blank_all = []
# print(final_line)
while True:
	line = fileobj.readline()
	if line:
		row_no += 1
		print(row_no, ":", line)
		# 関数の判定
		sub_pattern_def = re.findall(rejex_method_name, line)
		# print("def", sub_pattern_def)
		# 行頭のスペース・タブを抽出
		sub_pattern_all = re.findall(all_line_re, line)
		# print(f"all: {sub_pattern_all}")
		# if re.fullmatch(r'[ \t]*\n$', sub_pattern_all[0]) is not None:
		# 	print("blank")
		# sys.exit()
		# 空白行の場合、ブロックの終わりとみなさない
		# if re.fullmatch(blank_line_re, line) is not None:
		# 	head_blank_all.append("")
		# else:
		head_blank_all.append(sub_pattern_all[0])
		# print('head', head_blank_all) # debug
		# 関数を含む行か判定
		if len(sub_pattern_def) != 0:
			print('enter def')
			# stack_blankに行頭の空白を保存
			stack_blank.push(sub_pattern_def[0][0])
			# ブロックの最初の行番号を保存
			stack_start_line.push(row_no)
	else:
		break

for idx_def, blank_def in enumerate(reversed(stack_blank.stack)):
	# print("def", idx_def)
	# print(f"blank_def: '{blank_def}'")
	# print("len(blank_def)", len(blank_def))
	start_line = stack_start_line.pop()
	print("start_line: ", start_line)
	b = 0
	for idx_all, blank_all in enumerate(head_blank_all):
		# if idx_all + 1 <= stack_start_line.stack[-1]:
		# 関数より上の行は飛ばす
		if idx_all + 1 <= start_line:
			continue
		print("idx_all: ", idx_all)
		# 空白行は保留
		if re.fullmatch(r'[ \t]*\n$', blank_all) is not None:
			print("blank_all: ", blank_all)
			b += 1
			print("b: ", b)
		# ブロック抜けを判定
		elif len(blank_all) <= len(blank_def):
			# グローバル関数の場合
			if len(blank_def) == 0: 
				# blockの最初と最後の行番号をリストに保存
				line_glob.append([start_line, idx_all - b])
			# 内部関数の場合
			else:
				line_local.append([start_line, idx_all - b])
			break
		# 最後の関数が上の条件を満たさずに最後まで来た場合
		elif idx_all + 1 == len(head_blank_all):
			# グローバル関数の場合
			if len(blank_def) == 0:
				# blockの最初と最後の行番号をリストに保存
				line_glob.append([start_line, idx_all + 1])
			# 内部関数の場合
			else:
				line_local.append([start_line, idx_all + 1])
			break
		# ブロックを抜けてない場合
		else:
			b = 0

print("line_local ", line_local)
print("line_glob", line_glob)

### 空白行の挿入・削除 ###
# 消す行のインデックスを保存するリスト
del_lines = []
# 空白行を追加したい行間の内、より大きい行のインデックスを保存するリスト
add_lines = []
# Undone->True, Done->False
flag_local = np.full_like(line_local, True)
flag_glob = np.full_like(line_glob, True)
# ファイルの読込
with open(FILE_PATH) as f:
	txt = f.readlines()
	print("txt: ", txt)
	# ローカル関数
	for block in line_local:
		print("<block>", block)
		# ブロック開始行の1つ上の行のインデックス(ひとつ上なので-1, インデックスなのでさらに-1)
		above_b = block[0] - 2
		print("above_b: ", above_b)
		# ブロック開始行の1つ下の行のインデックス
		below_b = block[1]
		print("below_b: ", below_b)
		# ブロック開始行の1つ上にコメント行がある場合
		if re.fullmatch(r'\s*#.*', txt[above_b]) is not None:
			above_b -= 1
		# ブロック開始行の1つ上に空行がある場合
		if re.fullmatch(r'\s+', txt[above_b]) is not None:
			i = 1
			while True:
				# 注目している行が空行でない場合
				if re.fullmatch(r'\s+', txt[above_b - i]) is None:
					print("above_b - i + 1: ", above_b - i + 1)
					# ローカル関数ブロックの末行だった場合 -> あとまわし
					if above_b - i + 1 in [col[1] for col in line_local]:
						break
					# ブロックの上の空行が1行のみだった場合 -> 何もしない
					elif i == 1: 
						break
					# 通常の行の場合
					else:
						del_lines += [above_b - j for j in range(1, i)]	
						print("del_lines: ", del_lines)	
						break		
				i += 1
		# ブロック開始行の1つ上に空行でない行がある場合
		elif re.fullmatch(r'\s+', txt[above_b]) is None:
			print("not blank")
			add_lines.append(above_b + 1)

		# ブロック終了行の1つ下に空行がある場合
		if re.fullmatch(r'\s+', txt[below_b]) is not None:
			print("blank found")
			i = 1
			while True:
				# 注目している行が空行でない場合
				if re.fullmatch(r'\s+', txt[below_b + i]) is None:
					# 空白でなかった行の行番号を表示
					print("below_b + i + 1: ", below_b + i + 1)
					# グローバル関数ブロックの開始行だった場合
					if below_b + i + 1 in [col[0] for col in line_glob]:
						break
					# ブロックの下の空行が1行のみだった場合 -> 何もしない
					elif i == 1:
						break
					# それ以外
					else:
						del_lines += [below_b + j for j in range(1, i) if below_b + j not in del_lines]
						print("del_lines: ", del_lines)
						break
				i += 1
		# ブロック終了行の1つ下に空行でない行がある場合
		else:
			print("not blank")
			# グローバル関数ブロックの開始行だった場合
			if below_b + 1 in [col[0] for col in line_glob]:
				break
			else:
				if below_b + 1 not in del_lines:
					del_lines.append(below_b + 1)
				print("del_lines: ", del_lines)
				break





		# ブロック終了行の1つ下に空行でない行がある場合

# 	# グローバル関数

		# グローバル関数ブロックの開始行だった場合
		# if below_b + i + 1 in [col[0] for col in line_glob]:
		# 	if i == 2:
		# 		break
		# 	del_lines += [above_b - j + 1 for j in range(1, i)]	
		# 	# print("del_lines: ", del_lines)
		# 	break
	
# 					# ページ1行目だった場合
# 					elif above_b - i + 1 == 1:
# 						del


						
# 					elif txt[above_b]
# 					break
# 				elif above_b - i == 0:
# 				i += 1
print("del_lines: ", del_lines)
print("add_lines: ", add_lines)
# # コメント行の場合
# if re.fullmatch(r'\s*#.*', txt[above_b - i]) is not None:

# 	for block in line_local:
# 		if blockの下に空白行がある
			
# 		elif blockの下が空白行ではない
# 			blockの下に空白を挿入
# 		if blockの上に空白行が2つ以上ある
# 			余分な空白行を削除して1つにする
# 		elif blockの上が空白行ではない
# 			blockの上に空白を挿入

# 	for block in グローバル関数ブロックの集合
# 		if blockの下に空白行が3つ以上ある
# 			余分な空白行を削除して2つにする
# 		elif blockの下が空白行ではない
# 			blockの下に空白を挿入
# 		if blockの上に空白行が3つ以上ある
# 			余分な空白行を削除して2つにする
# 		elif blockの上が空白行ではない
# 			blockの上に空白を挿入


