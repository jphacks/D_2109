# -*- coding: utf-8 -*-
import re
import sys
import numpy as np
import pprint

FILE_PATH = "output.py"
SENTINEL = 1000000

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

### def・classブロックのサーチ ### 
stack_blank = MyStack()
stack_start_line = MyStack()
line_glob = []
line_local = []
row_no = 0
rejex_method_name = "(^[ \t]*)def[ \t]+(\w+)[ \t]*\(.*\)[ \t]*:"
rejex_class_name = "(^[ \t]*)class\s+.*"
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
		# クラスの判定
		sub_pattern_class = re.findall(rejex_class_name, line)
		print("class", sub_pattern_class)
		# 行頭のスペース・タブを抽出
		sub_pattern_all = re.findall(all_line_re, line)
		head_blank_all.append(sub_pattern_all[0])
		# 関数を含む行か判定
		if len(sub_pattern_def) != 0:
			print('entered def')
			# stack_blankに行頭の空白を保存
			stack_blank.push(sub_pattern_def[0][0])
			# ブロックの最初の行番号を保存
			stack_start_line.push(row_no)
		# クラスを含む行か判定
		elif len(sub_pattern_class) != 0:
			print('entered class')
			# stack_blankに行頭の空白を保存
			stack_blank.push(sub_pattern_class[0])
			# ブロックの最初の行番号を保存
			stack_start_line.push(row_no)
	else:
		break

for blank_def in reversed(stack_blank.stack):
	print("ブランクデフ" , type(blank_def))
	# print("def", idx_def)
	# print(f"blank_def: '{blank_def}'")
	# print("len(blank_def)", len(blank_def))
	start_line = stack_start_line.pop()
	print("start_line: ", start_line)
	# bはブランク数
	b = 0
	# sys.exit()
	for idx_all, blank_all in enumerate(head_blank_all):
		print("ブランクオール", type(blank_all))
		# if idx_all + 1 <= stack_start_line.stack[-1]:
		# 関数より上の行は飛ばす
		if idx_all + 1 <= start_line:
			continue
		print("idx_all: ", idx_all)
		# 最終行の場合
		if idx_all + 1 == len(head_blank_all):
			# 空白行の場合
			if re.search(r'\n$', blank_all) is not None:
				print('空白行だよ')
				# グローバル関数・クラスの場合
				if len(blank_def) == 0:
					# blockの最初と最後の行番号をリストに保存
					line_glob.append([start_line, idx_all - b])
					print("exit global")
					break
				# 内部関数の場合
				else:
					line_local.append([start_line, idx_all - b])
					print("exit local")
					break
			# 空白行でない場合
			else:
				print('空白行じゃないよ')
				# グローバル関数・クラスの場合
				if len(blank_def) == 0:
					# blockの最初と最後の行番号をリストに保存
					line_glob.append([start_line, idx_all + 1])
					print("exit global")
					break
				# 内部関数の場合
				else:
					line_local.append([start_line, idx_all + 1])
					print("exit local")
					break

		# 空白行は保留
		elif re.fullmatch(r'[ \t]*\n$', blank_all) is not None:
			print("空白行")
			# print("blank_all: ", blank_all)
			b += 1
			print("b: ", b)
		# ブロック抜けを判定
		elif len(blank_all) <= len(blank_def):
			# グローバル関数・クラスの場合
			if len(blank_def) == 0: 
				# blockの最初と最後の行番号をリストに保存
				line_glob.append([start_line, idx_all - b])
				print("exit global")
			# 内部関数の場合
			else:
				line_local.append([start_line, idx_all - b])
				print("exit local")
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

print("txt_len", len(txt))

### ローカル関数 ### 
for block in line_local:
	print("<block>", block)
	# ブロック開始行の1つ上の行のインデックス(ひとつ上なので-1, インデックスなのでさらに-1)
	above_b = block[0] - 2
	print("above_b: ", above_b)
	# ブロック開始行の1つ下の行のインデックス
	below_b = block[1]
	print("below_b: ", below_b)
	# ブロック開始行の1つ上にコメント行がある場合
	if re.search(r'#', txt[above_b]) is not None:
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
					# グローバル関数・クラスの開始行だった場合
					if above_b - i + 1 in [col[0] for col in line_glob]:
						s = 0
					# それ以外
					else:
						s = 1
					del_lines += [above_b - j for j in range(s, i)]	
					print("del_lines: ", del_lines)	
					break		
			i += 1
	# ブロック開始行の1つ上に空行でない行がある場合
	elif re.fullmatch(r'\s+', txt[above_b]) is None:
		print("not blank")
		# グローバル関数・クラスの開始行だった場合
		if above_b + 1 in [col[0] for col in line_glob]:
			pass
		else:
			add_lines.append(above_b + 1)
		print("add_lines: ", add_lines)
	# ブロック終了行が最終行の場合
	if below_b >= len(txt) - 1:
		print("さいしゅう")
		pass
	# ブロック終了行の1つ下に空行がある場合
	elif re.fullmatch(r'\s+', txt[below_b]) is not None:
		print("blank found")
		i = 1
		while True:
			print("i: ", i)
			# 注目している行が最終行の場合 -> ブロック下の空白行すべて消す
			if below_b + i + 1 == len(head_blank_all):
				del_lines += [below_b + j for j in range(0, i) if below_b + j not in del_lines]
				print("del_lines: ", del_lines)
				break
			# 注目している行が空行でない
			if re.fullmatch(r'\s+', txt[below_b + i]) is None:
				# 空白でなかった行の行番号を表示
				print("below_b + i + 1: ", below_b + i + 1)
				# グローバル関数・クラスブロックの開始行だった場合
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
		# グローバル関数・クラスブロックの開始行だった場合
		if below_b + 1 in [col[0] for col in line_glob]:
			pass
		else:
			if below_b not in add_lines:
				add_lines.append(below_b)
			print("add_lines: ", add_lines)

### グローバル関数 ### 
print("<<<global>>>")
for block in line_glob:
	print("<block>", block)
	# ブロック開始行の1つ上の行のインデックス(ひとつ上なので-1, インデックスなのでさらに-1)
	above_b = block[0] - 2
	print("above_b: ", above_b)
	# ブロック最終 行の1つ下の行のインデックス
	below_b = block[1]
	print("below_b: ", below_b)
	# ブロック開始行の1つ上にコメント行がある場合
	if re.search(r'#', txt[above_b]) is not None:
		print("コメント見つけた")
		above_b -= 1
	else:
		print("見つからない")
	# ブロック開始行が1行目の場合
	if above_b == -1:
		print("一番上")
		pass
	# ブロック開始行の1つ上に空行がある場合
	elif re.fullmatch(r'\s+', txt[above_b]) is not None:
		i = 1
		while True:
			# 注目している行が1行目の場合 -> ブロック上の空白行すべて消す
			if above_b - i + 1 == len(head_blank_all):
				del_lines += [above_b - j for j in range(0, i) if above_b - j not in del_lines]
				print("del_lines: ", del_lines)
				break
			# 注目している行が空行でない場合
			elif re.fullmatch(r'\s+', txt[above_b - i]) is None or below_b - i == 0:
				print("above_b - i + 1: ", above_b - i + 1)
				# グローバル関数・クラスブロックの末行だった場合 -> あとまわし
				if above_b - i + 1 in [col[1] for col in line_glob]:
					print("あとまわし")
					break
				# ブロックの上の空行が1行のみだった場合 -> 一行追加で挿入
				elif i == 1:
					add_lines += [above_b + 1]
					print("1行のみ_add_lines: ", add_lines)
				# ブロックの上の空行が2行のみだった場合 -> 何もしない
				elif i == 2: 
					break
				# それ以外
				else:
					del_lines += [above_b - j for j in range(1, i - 1)]
					print("del_lines: ", del_lines)	
					break		
			i += 1
	# ブロック開始行の1つ上が空行でない場合(above_bの値によって挙動が変わるのでelseにはしない)
	elif re.fullmatch(r'\s+', txt[above_b]) is None:
		print("not blank")
		add_lines += [above_b + 1, above_b + 1]
		print("add_lines: ", add_lines)
	# ブロック終了行が最終行の場合
	if below_b >= len(txt) - 1:
		print("さいしゅうぎょう")
		pass
	# ブロック終了行の1つ下に空行がある場合
	elif re.fullmatch(r'\s+', txt[below_b]) is not None:
		print("blank found")
		i = 1
		while True:
			# 注目している行が最終行の場合 -> ブロック下の空白行すべて消す
			if below_b + i + 1 == len(head_blank_all):
				print("最終行")
				del_lines += [below_b + j for j in range(0, i + 1) if below_b + j not in del_lines]
				print("del_lines: ", del_lines)
				break
			# 注目している行が空行でない
			if re.fullmatch(r'\s+', txt[below_b + i]) is None:
				# 空白でなかった行の行番号を表示
				print("below_b + i + 1: ", below_b + i + 1)
				# 最終行の場合 -> 空白行すべて削除
				if below_b + i + 1 == len(head_blank_all):
					print("最終行")
					del_lines += [above_b + j for j in range(0, i) if above_b + j not in del_lines]
					print("del_lines: ", del_lines)
					break
				# ブロックの下の空行が2行だった場合 -> 何もしない
				elif i == 2:
					break
				# ブロックの上の空行が1行のみだった場合 -> 一行追加で挿入
				elif i == 1:
					add_lines += [below_b]
					print("1行のみ_add_lines: ", add_lines)
					break
				# それ以外(3行以上)
				else:
					del_lines += [below_b + j for j in range(0, i - 2) if below_b + j not in del_lines]
					print("del_lines: ", del_lines)
					break
			i += 1
	# ブロック終了行の下が空行でない場合
	else:
		print("not blank, insert")
		add_lines += [below_b, below_b]
		print("add_lines: ", add_lines)		
	# else:
	# 	print("not blank")
	# 	if below_b + 1 not in del_lines:
	# 		del_lines.append(below_b + 1)
	# 	print("del_lines: ", del_lines)
	# 	break

del_lines.sort()
add_lines.sort()
del_lines.append(SENTINEL)
add_lines.append(SENTINEL)
i = 0
j = 0

print("del_lines: ", del_lines)
print("add_lines: ", add_lines)

while True:
	if i + 1 == len(del_lines) and j + 1 == len(add_lines):
		print("complete!")
		break
	elif del_lines[i] < add_lines[j]:
		# 行の削除
		txt.pop(del_lines[i])
		del_lines = [el - 1 for el in del_lines]
		add_lines = [el - 1 for el in add_lines]
		i += 1
	else:
		# 行の追加
		txt.insert(add_lines[j], "\n")
		del_lines = [el + 1 for el in del_lines]
		add_lines = [el + 1 for el in add_lines]
		j += 1

# pprint.pprint(txt)

w_path = "output2.py"

with open(w_path, mode='w') as f:
    f.writelines(txt)
 

