import json
import re

from constants import REJEX_METHOD_NAME, REJEX_METHOD_NAME_BACK, REJEX_CLASS_NAME, TRIM_INFO_STYLE_BLANK_FALSE
from method.is_comile_to_dic import is_comile_to_dic
from method.scan_indent_config import scan_indent_config
from method.naming import scan_naming_method_class, scan_naming_value
from method.import_part.split_import import split_import
from method.import_part.group_sort_impot import group_sort_import
from method.general import strip_blank_line, add_newline_char, get_start_blank, make_args
from method.stack import Stack


# 1行ごとに 文字数カウント
def scan_style_count_word(lst, op_count_word):
  s_warn_count = 0
  if not op_count_word['action']:
    return lst
  lst_cp = []
  pattern = re.compile(r'^[^\\]*\\$')
  
  buffer = []
  length = op_count_word["length"] + 1
  for line in lst:
    match_flag = bool(pattern.match(line))
    # 行頭のインデントを取得
    starts_blank = get_start_blank(line)
    # もし'/'で終わってたら状態を保存
    if match_flag:
      #print("match!!")
      buffer.append({'blank': starts_blank, 'mes': line})
    if len(line)>= length and (not match_flag):
      blank = starts_blank if len(buffer) == 0 else buffer[0]['blank']
      TRIM_WARNING_STYLE_COUNT_WARD = f'# [trim] Warning: 1行あたりの行数は最大{op_count_word["length"]}文字です.適切な位置で折り返してください.'
      lst_cp.append(blank + TRIM_WARNING_STYLE_COUNT_WARD)
      s_warn_count += 1
      for dic in buffer:
        lst_cp.append(dic['mes'])
      lst_cp.append(line)
      buffer = []
    # 状態の初期化
    if not match_flag and len(line)<length:
      buffer = []
      lst_cp.append(line)
  return {
    'lst': lst_cp,
    's_warn_count': s_warn_count
  }


# 前後の空白を調整(1行分)
def check_operators_space(line: str, method_naming, class_naming):
    #print(f"met:{method_naming.method_lst}")
    #print(class_naming.class_lst)
    strip_str = line.strip()
    # コメント行や空文字のみの行はpass
    if strip_str.startswith('#') or strip_str == '':
      return line

    if not (re.findall(REJEX_METHOD_NAME, line)
        or re.findall(REJEX_METHOD_NAME_BACK, line)
        or re.findall(REJEX_CLASS_NAME, line)):
        #REJEX = (f'(\([^)]*\))')
        #remove_str_line = re.sub(REJEX_STRING_SINGLE_STRICT + '|' + REJEX_STRING_DOUBLE_STRICT + '|' + REJEX_COMMENT, '', line)
        
        for s in list(set(method_naming.method_lst)):
          REJEX = (f'{s}\s*\(.+\)')
          if re.findall(REJEX, line):
            args = make_args(re.findall(REJEX, line)[0])
            strip_str = re.sub(f'{s}\s*\(.+\)', args, strip_str)

        for s in list(set(class_naming.class_lst)):
          REJEX = (f'{s}\s*\(.+\)')
          if re.findall(REJEX, line):
            args = make_args(re.findall(REJEX, line)[0])
            strip_str = re.sub(f'{s}\s*\(.+\)', args, strip_str)

        # 行のword内に' 'が2つ以上入っていたら' '1つにする
        strip_str_lst = [s for s in re.split('\s', strip_str) if s != '']
        #print(strip_str_lst)
        n = len(strip_str_lst)
        #print(n)
        #REJEX = "([\w=]+( {2,}))" * n
        # 行頭のインデントを取得
        s = get_start_blank(line)
        for i, st in enumerate(strip_str_lst):
          if i != len(strip_str_lst):
            s += st + ' '
          else:
            s += st
        line = s
        #print("###########")
        #print(line)

        # スライス内の演算子の前後にはスペースを追加しない
        if(not re.findall('\\[.*:.*\\]', line)):
            if(not re.findall('([a-zA-Z0-9]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([a-zA-Z0-9]*)',line)):
                line = re.sub(
                    '([a-zA-Z0-9]*)([\s]*)(<>|<=|>=|is not|not in|-=|==|\\+=|!=|=|\\+|-|\\*|/|%|<|>|and|or|not|in|is)([\s]*)([a-zA-Z0-9]*)',
                    '\\1 \\3 \\5',
                    line)
        # lineの末尾を確認

    return line


def blank_lines(lst, opt):
	# 番兵
	SENTINEL = 1000000

	### def・classブロックのサーチ ### 
	stack_blank = Stack()
	stack_start_line = Stack()

	line_glob = []
	line_local = []
	head_blank_all = []

	row_no = 0

	# rejex_method_name = "(^[ \t]*)def[ \t]+(\w+)[ \t]*\(.*\)[ \t]*:"
	rejex_method_name = "(^[ \t]*)def[ \t]+(\w+)[ \t]*\(.*\).*"
	rejex_class_name = "(^[ \t]*)class\s+.*"
	all_line_re = "(^[ \t\n]*)"

	# 関数・クラスブロックの開始行を探索
	for line in lst:
		row_no += 1
		#printf"{row_no}行目")
		# 関数の判定
		sub_pattern_def = re.findall(rejex_method_name, line)
		# クラスの判定
		sub_pattern_class = re.findall(rejex_class_name, line)
		# 行頭のスペース・タブを抽出
		sub_pattern_all = re.findall(all_line_re, line)
		head_blank_all.append(sub_pattern_all[0])
		# 関数を含む行か判定
		if len(sub_pattern_def) != 0:
			#print'entered def')
			# stack_blankに行頭の空白を保存
			stack_blank.push(sub_pattern_def[0][0])
			# ブロックの最初の行番号を保存
			stack_start_line.push(row_no)
		# クラスを含む行か判定
		elif len(sub_pattern_class) != 0:
			#print'entered class')
			# stack_blankに行頭の空白を保存
			stack_blank.push(sub_pattern_class[0])
			# ブロックの最初の行番号を保存
			stack_start_line.push(row_no)


	# 関数・クラスブロックの終了行を探索
	for blank_def in reversed(stack_blank.stack):
		start_line = stack_start_line.pop()
		#print"start_line: ", start_line)
		# 空白行数のカウント用
		b = 0
		for idx_all, blank_all in enumerate(head_blank_all):
			# 関数より上の行は飛ばす
			if idx_all + 1 <= start_line:
				continue
			#printf"{idx_all}行目")
			# 最終行の場合
			if idx_all + 1 == len(head_blank_all):
				#print"最終行です")
				# 空白行の場合
				if re.search(r'\n$', blank_all) is not None:
					#print'空白行だよ')
					# グローバル関数・クラスの場合
					if len(blank_def) == 0:
						# blockの最初と最後の行番号をリストに保存
						line_glob.append([start_line, idx_all - b])
						#print"exited from global")
						break
					# 内部関数の場合
					else:
						line_local.append([start_line, idx_all - b])
						#print"exited from local")
						break
				# 空白行でない場合
				else:
					#print'空白行じゃないよ')
					# グローバル関数・クラスの場合
					if len(blank_def) == 0:
						# blockの最初と最後の行番号をリストに保存
						line_glob.append([start_line, idx_all + 1])
						#print"exited from global")
						break
					# 内部関数の場合
					else:
						line_local.append([start_line, idx_all + 1])
						#print"exited from local")
						break

			# 空白行は保留
			elif re.fullmatch(r'[ \t]*\n$', blank_all) is not None:
				#print"空白行・保留")
				b += 1
				#print"b: ", b)
			# ブロック抜けを判定
			elif len(blank_all) <= len(blank_def):
				# グローバル関数・クラスの場合
				if len(blank_def) == 0: 
					# blockの最初と最後の行番号をリストに保存
					line_glob.append([start_line, idx_all - b])
					#print"exited from global")
				# 内部関数の場合
				else:
					line_local.append([start_line, idx_all - b])
					#print"exited from local")
				break

			# ブロックを抜けてない場合
			else:
				b = 0

	#print"line_local ", line_local)
	#print"line_glob", line_glob)

	if not opt['class_or_global_func']['action']:
		line_glob.clear()
	if not opt['method']['action']:
		line_local.clear()

	### 空白行の挿入・削除 ###

	# 消す行のインデックスを保存するリスト
	del_lines = []
	# 空白行を追加したい行間の内、より大きい行のインデックスを保存するリスト
	add_lines = []

	## ローカル関数 ##
	if opt['method']['action']:
		for block in line_local:
			#print"block: ", block)
			# ブロック開始行の1つ上の行のインデックス(ひとつ上なので-1, インデックスなのでさらに-1)
			above_b = block[0] - 2
			#print"above_b: ", above_b)
			# ブロック開始行の1つ下の行のインデックス
			below_b = block[1]
			#print"below_b: ", below_b)
			# ブロック開始行の1つ上にコメント行がある場合
			if re.search(r'#', lst[above_b]) is not None:
				above_b -= 1
			# ブロック開始行の1つ上に空行がある場合
			if re.fullmatch(r'\s+', lst[above_b]) is not None:
				i = 1
				while True:
					# 注目している行が空行でない場合
					if re.fullmatch(r'\s+', lst[above_b - i]) is None:
						#print"above_b - i + 1: ", above_b - i + 1)
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
							#print"del_lines: ", del_lines)	
							break		
					i += 1
			# ブロック開始行の1つ上に空行でない行がある場合
			elif re.fullmatch(r'\s+', lst[above_b]) is None:
				#print"not blank")
				# グローバル関数・クラスの開始行だった場合
				if above_b + 1 in [col[0] for col in line_glob]:
					pass
				else:
					add_lines.append(above_b + 1)
				#print"add_lines: ", add_lines)
			# ブロック終了行が最終行の場合
			if below_b >= len(lst) - 1:
				#print"最終")
				pass
			# ブロック終了行の1つ下に空行がある場合
			elif re.fullmatch(r'\s+', lst[below_b]) is not None:
				#print"blank found")
				i = 1
				while True:
					#print"i: ", i)
					# 注目している行が最終行の場合 -> ブロック下の空白行すべて消す
					if below_b + i + 1 == len(head_blank_all):
						del_lines += [below_b + j for j in range(0, i) if below_b + j not in del_lines]
						#print"del_lines: ", del_lines)
						break
					# 注目している行が空行でない
					if re.fullmatch(r'\s+', lst[below_b + i]) is None:
						# 空白でなかった行の行番号を表示
						#print"below_b + i + 1: ", below_b + i + 1)
						# グローバル関数・クラスブロックの開始行だった場合
						if below_b + i + 1 in [col[0] for col in line_glob]:
							break
						# ブロックの下の空行が1行のみだった場合 -> 何もしない
						elif i == 1:
							break
						# それ以外
						else:
							del_lines += [below_b + j for j in range(1, i) if below_b + j not in del_lines]
							#print"del_lines: ", del_lines)
							break
					i += 1
			# ブロック終了行の1つ下に空行でない行がある場合
			else:
				#print"not blank")
				# グローバル関数・クラスブロックの開始行だった場合
				if below_b + 1 in [col[0] for col in line_glob]:
					pass
				else:
					if below_b not in add_lines:
						add_lines.append(below_b)
					#print"add_lines: ", add_lines)


	## グローバル関数 ## 
	if opt['class_or_global_func']['action']:
		#print"<<<global>>>")
		for block in line_glob:
			#print("block: ", block)
			# ブロック開始行の1つ上の行のインデックス(ひとつ上なので-1, インデックスなのでさらに-1)
			above_b = block[0] - 2
			#print("above_b: ", above_b)
			# ブロック最終 行の1つ下の行のインデックス
			below_b = block[1]
			#print("below_b: ", below_b)
			# ブロック開始行の1つ上にコメント行がある場合
			if re.search(r'#', lst[above_b]) is not None:
				#print("コメント見つけた")
				above_b -= 1
			else:
				print("見つからない")
			# ブロック開始行が1行目の場合
			if above_b == -1:
				#print("一番上")
				pass
			# ブロック開始行の1つ上に空行がある場合
			elif re.fullmatch(r'\s+', lst[above_b]) is not None:
				i = 1
				while True:
					# 注目している行が1行目の場合 -> ブロック上の空白行すべて消す
					if above_b - i + 1 == len(head_blank_all):
						del_lines += [above_b - j for j in range(0, i) if above_b - j not in del_lines]
						#print("del_lines: ", del_lines)
						break
					# 注目している行が空行でない場合
					elif re.fullmatch(r'\s+', lst[above_b - i]) is None or below_b - i == 0:
						#print("above_b - i + 1: ", above_b - i + 1)
						# グローバル関数・クラスブロックの末行だった場合 -> あとまわし
						if above_b - i + 1 in [col[1] for col in line_glob]:
							#print("あとまわし")
							break
						# ブロックの上の空行が1行のみだった場合 -> 一行追加で挿入
						elif i == 1:
							add_lines += [above_b + 1]
							#print("1行のみ_add_lines: ", add_lines)
						# ブロックの上の空行が2行のみだった場合 -> 何もしない
						elif i == 2: 
							break
						# それ以外
						else:
							del_lines += [above_b - j for j in range(1, i - 1)]
							#print("del_lines: ", del_lines)	
							break		
					i += 1
			# ブロック開始行の1つ上が空行でない場合(above_bの値によって挙動が変わるのでelseにはしない)
			elif re.fullmatch(r'\s+', lst[above_b]) is None:
				#print("not blank")
				add_lines += [above_b + 1, above_b + 1]
				#print("add_lines: ", add_lines)
			# ブロック終了行が最終行の場合
			if below_b >= len(lst) - 1:
				#print("さいしゅうぎょう")
				pass
			# ブロック終了行の1つ下に空行がある場合
			elif re.fullmatch(r'\s+', lst[below_b]) is not None:
				#print("blank found")
				i = 1
				while True:
					# 注目している行が最終行の場合 -> ブロック下の空白行すべて消す
					if below_b + i + 1 == len(head_blank_all):
						#print("最終行")
						del_lines += [below_b + j for j in range(0, i + 1) if below_b + j not in del_lines]
						#print("del_lines: ", del_lines)
						break
					# 注目している行が空行でない
					if re.fullmatch(r'\s+', lst[below_b + i]) is None:
						# 空白でなかった行の行番号を表示
						#print("below_b + i + 1: ", below_b + i + 1)
						# 最終行の場合 -> 空白行すべて削除
						if below_b + i + 1 == len(head_blank_all):
							#print("最終行")
							del_lines += [above_b + j for j in range(0, i) if above_b + j not in del_lines]
							#print("del_lines: ", del_lines)
							break
						# ブロックの下の空行が2行だった場合 -> 何もしない
						elif i == 2:
							break
						# ブロックの上の空行が1行のみだった場合 -> 一行追加で挿入
						elif i == 1:
							add_lines += [below_b]
							#print("1行のみ_add_lines: ", add_lines)
							break
						# それ以外(3行以上)
						else:
							del_lines += [below_b + j for j in range(0, i - 2) if below_b + j not in del_lines]
							#print("del_lines: ", del_lines)
							break
					i += 1
			# ブロック終了行の下が空行でない場合
			else:
				#print("lst[below_b]", lst[below_b])
				#print("not blank, insert")
				if below_b not in add_lines:
					add_lines += [below_b, below_b]
				#print("add_lines: ", add_lines)		

	del_lines.sort()
	add_lines.sort()

	del_lines.append(SENTINEL)
	add_lines.append(SENTINEL)
	i = 0
	j = 0

	#print("del_lines: ", del_lines)
	#print("add_lines: ", add_lines)

	while True:
		if i + 1 == len(del_lines) and j + 1 == len(add_lines):
			#print("complete!")
			break
		elif del_lines[i] < add_lines[j]:
			# 行の削除
			lst.pop(del_lines[i])
			del_lines = [el - 1 for el in del_lines]
			add_lines = [el - 1 for el in add_lines]
			i += 1
		else:
			# 行の追加
			lst.insert(add_lines[j], "\n")
			del_lines = [el + 1 for el in del_lines]
			add_lines = [el + 1 for el in add_lines]
			j += 1

	return lst


# 前後の空白を調整(走査)
def scan_operators_space(lst, method_naming, class_naming):
  lst_cp = []
  for line in lst:
    lst_cp.append(check_operators_space(line, method_naming, class_naming))
  return lst_cp


def make_ss(flag_snake, flag_cap):
  ss = ' '
  if not (flag_snake or flag_cap):
    ss += "False"
  if flag_cap:
    ss += "CapWords"
  if flag_snake:
    s = '/' if flag_cap else '' 
    ss += s + "snake"
  return ss


def lambda_handler(event, context):
    #body_dict = json.loads(event['body'])
    body_dict = event['body']
    lst_cp = body_dict['code_lst']
    op = body_dict['op']

    INDENT_TAB_NUM = op['style_check']['indent']['tab_num']

    # コード配列の各要素の行末に改行文字
    lst_cp = add_newline_char(lst_cp)
    
    # compileが通るか確認
    compile_dic = is_comile_to_dic(lst_cp)

    if not compile_dic['flag']:
      return {
        'statusCode': 200,
        'body': json.dumps({
            'code_lst': [compile_dic['error']]
          })
      }
    
    # 空行をきれいにする
    lst_cp = strip_blank_line(lst_cp)

    # 末尾空白文字の削除
    lst_cp = list(map(lambda x: x.rstrip(), lst_cp))

    # タブ文字を' '*INDENT_TAB_NUMに置き換え
    lst_cp = list(map(lambda x: re.sub('\t', ' '*INDENT_TAB_NUM, x), lst_cp))

    # import部のスプリット
    lst_cp = split_import(lst_cp)
    
    # import部のグルーピング・ソーティング
    lst_cp = group_sort_import(lst_cp, op['import_check'])

    # 走査して、適切なインデントに調節していく 
    lst_cp = scan_indent_config(lst_cp, op['style_check']['indent'])
    
    # 走査して関数とクラスの整形を行う
    lst_dic = scan_format_method_class(lst_cp, op['style_check']['blank_format'])
    lst_cp = lst_dic['lst']
    def_blank_num = lst_dic['def-blank']
    class_blank_num = lst_dic['class-blank']
    
    # 走査: 関数とクラスの命名規則チェック
    lst_dic = scan_naming_method_class(lst_cp, op['naming_check'])
    lst_cp = lst_dic['lst']
    method_naming = lst_dic['method_naming']
    class_naming = lst_dic['class_naming']



    # 文字数警告
    lst_dic = scan_style_count_word(lst_cp, op['style_check']['count_word'])
    lst_cp = lst_dic['lst']
    #print(lst_cp)
    s_warn_count = lst_dic['s_warn_count']
    # 前後の空白を調整
    lst_cp = scan_operators_space(lst_cp, method_naming, class_naming)
    
    # 改行コードを追加
    lst_cp = list(map(lambda x: x + '\n', lst_cp))

    # 変数の解析と命名規則チェック
    lst_cp = scan_naming_value(lst_cp, op['naming_check'])
    # インデント文字
    indent = '\t' if op['style_check']['indent']['type'] == '\t' else ' '*op['style_check']['indent']['num']
    
    INFO_MES_LIST = [
      '"""©trim 整形実行後ファイル\n',
      indent + '・空白整形の設定',
      indent * 2 + f'関数: {def_blank_num}箇所\n',
      indent * 2 + f'クラス: {class_blank_num}箇所\n',
      indent + '・行あたりの文字数設定 - ',
      indent * 2 + f'[警告] {s_warn_count}箇所\n',
      indent + '・クラス・グローバル関数間の間隔 - ',
      indent + '・メソッド間の間隔 - ',
      indent + '・importの設定\n',
      indent * 2 + f'・グルーピング: ',
      indent * 2 + f'・アルファベットソート: ',
      indent + '・命名規則 - ',
      '"""\n',
    ]
    # 上からopに応じて変形し、=> INFO_MES_LIST_CPへ => lst_cpに戻す
    INFO_MES_LIST_CP = []
    i = 0
    while True:
      elem = INFO_MES_LIST[i]
      #print(elem)
      if elem.startswith(indent + '・空白整形'):
        flag = op['style_check']['blank_format']['action']
        elem += f"\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        if not flag:
          INFO_MES_LIST_CP.append(indent * 2 + TRIM_INFO_STYLE_BLANK_FALSE + '\n')
          i+=2
        continue
      if elem.startswith(indent + '・行あたりの文字数設定'):
        flag = op['style_check']['count_word']['action']
        if flag:
          elem += f"{op['style_check']['count_word']['length']}文字\n"
        else:
           elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent + '・クラス・グローバル関数間の間隔'):
        flag = op['style_check']['line_space']['class_or_global_func']
        if flag:
          elem += f"2文字\n"
        else:
          elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent + '・メソッド間の間隔'):
        flag = op['style_check']['line_space']['method']
        if flag:
          elem += f"1文字\n"
        else:
          elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent*2 + '・グルーピング'):
        flag = op['import_check']['grouping']
        elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent*2 + '・アルファベットソート'):
        flag = op['import_check']['sorting']
        elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent + '・命名規則'):
        INFO_MES_LIST_CP.append(elem + '\n')
        class_snake_flag = op['naming_check']['class_case']['snake']
        method_snake_flag = op['naming_check']['method_case']['snake']
        value_snake_flag = op['naming_check']['value_case']['snake']
        class_cap_flag = op['naming_check']['class_case']['CapWords']
        method_cap_flag = op['naming_check']['method_case']['CapWords']
        value_cap_flag = op['naming_check']['value_case']['CapWords']
        
        ss_class = make_ss(class_snake_flag, class_cap_flag)
        ss_method = make_ss(method_snake_flag, method_cap_flag)
        ss_value = make_ss(value_snake_flag, value_cap_flag)
        
        INFO_MES_LIST_CP.append(indent * 2 + f'クラス: ' + ss_class +'\n')
        INFO_MES_LIST_CP.append(indent * 2 + f'関数: ' + ss_method +'\n')
        INFO_MES_LIST_CP.append(indent * 2 + f'変数: ' + ss_value +'\n')
        i += 1
        continue
      INFO_MES_LIST_CP.append(elem)
      i += 1
      if i == len(INFO_MES_LIST):
        break
  
    INFO_MES_LIST_CP.extend(lst_cp)
    lst_cp = INFO_MES_LIST_CP
    
    # タブ文字設定の場合は半角X個をタブ文字に変換
    if op['style_check']['indent']['type'] == '\t':
      lst_cp = list(map(lambda x: re.sub(' '*op['style_check']['indent']['tab_num'], '\t', x), lst_cp))
        
    # 行間の調整
    lst_cp = blank_lines(lst_cp, op['style_check']['line_space'])

    """f = open('output/output.py', 'w') 
    f.writelines(lst_cp)
    f.close()"""

    # TODO implement
    return {
      'statusCode': 200,
      'body': json.dumps({
          'code_lst': lst_cp
        })
    }

# ローカルのみ
"""fileobj = open("input/dirty_code.py", "r", encoding="utf_8")
lst = []
event = {}
while True:
  line = fileobj.readline()
  if line:
      lst.append(line)
  else:
    break
with open('rule.json') as json_data:
  op = json.load(json_data)
  # bodyを文字列として送る(POST通信を想定)
  event['body'] = json.dumps({
    'code_lst': lst,
    'op': op
  })
  lambda_handler((event), None)"""