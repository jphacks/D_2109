import json
import re
import traceback
import keyword
from botocore.vendored import requests

# ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
#  'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for',
#  'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
#  'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

REJEX_METHOD_NAME = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*):"
REJEX_METHOD_NAME_BACK = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*)->([ |\t]*)(\w+)([ |\t]*):"
REJEX_CLASS_NAME = "class([ |\t]*)(\w+)([ |\t]*)(\((.*)\))*([ |\t]*):"

REJEX_STRING_DOUBLE = "\s*\".*\"\s*"
REJEX_STRING_SINGLE = "\s*\'.*\'\s*"
REJEX_COMMENT = "\s*#.*\s*\n\s*"

TRIM_WARNING_NAMING_METHOD_ALL = "# [trim] Warning: 関数名に大文字とアンダーバーを同時に含められません."
TRIM_WARNING_NAMING_METHOD_SNAKE = "# [trim] Warning: 関数名に大文字は含められません."
TRIM_WARNING_NAMING_METHOD_CAPWORDS = "# [trim] Warning: 関数名にアンダーバーは含められません."

TRIM_WARNING_NAMING_CLASS_ALL = "# [trim] Warning: クラス名に大文字とアンダーバーを同時に含められません."
TRIM_WARNING_NAMING_CLASS_SNAKE = "# [trim] Warning: クラス名に大文字は含められません."
TRIM_WARNING_NAMING_CLASS_CAPWORDS = "# [trim] Warning: クラス名にアンダーバーは含められません."

TRIM_INFO_STYLE_BLANK_FALSE = "Info: PEP8に基づく、空白の整形設定を行う事を推奨します."
TRIM_INFO_STYLE_IMPORT_GROUP = "# [trim] Info: グルーピング済みです."
TRIM_INFO_STYLE_IMPORT_SORT = "# [trim] Info: アルファベットソート済みです."

RESERVED_WORDS = keyword.kwlist
OTHER_WORDS = ['Exception']

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

# スタックの定義(by 刀祢)
class MyStack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        result = self.stack[-1]  # 末尾の要素を変数に取り出す
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する

# スタックの定義
class MyStack_Indent:
    def __init__(self, n):
        self.stack = [0]
    def get_top(self):
      return self.stack[-1]
    def get_reverse_lst(self):
        return reversed(self.stack)
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        result = self.stack[-1]  # 末尾の要素を変数に取り出す
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する

# コンパイルが通るかどうかを確認
def is_comile_to_dic(lst):
  try:
    line = ''.join(lst)
    compile(line, '', 'exec')
    return {'flag': True}
  except Exception as e:
      return {'flag': False, 'error': str(traceback.format_exc())}

# indent設定に合わせて\t=>' '*X文字にする
def scan_indent_config(lst, op_indent):
  INDENT_TAB_NUM = op_indent['tab_num']
  if op_indent['type'] == '\t':
    INDENT_NUM = op_indent['tab_num']
  else:
    INDENT_NUM = op_indent['num']
  
  # 末尾文字の削除
  lst_cp = list(map(lambda x: x.rstrip(), lst))

  # タブ文字を' '*INDENT_TAB_NUMに置き換え
  lst_cp = list(map(lambda x: re.sub('\t', ' '*INDENT_TAB_NUM, x), lst_cp))
  
  stack_indent = MyStack_Indent(0)
  stack = MyStack_Indent(0)

  bef = 0
  lst_after = []
  for row_no, line in enumerate(lst_cp, 1):
      #print(line)
      str_line = line
      # もし空行ならindentをstack_indentのheadに合わせる
      if re.match(r"$ *^", str_line):
          str_line = stack_indent.get_top() * ' '
      aft = re.match(r" *", str_line).end()
      
      
      #print(f"bef: {bef}")
      #print(f"aft: {aft}")
      
      # コメント行は無視
      if str_line.startswith("#"):
          lst_after.append(str_line)
          continue
      if bef > aft:
        for i, elem in enumerate(stack.get_reverse_lst()):
            #print(elem)
            if elem == aft:
                #print(f"pop数: {i}")
                # この時のiがpop数
                for j in range(i):
                    stack_indent.pop()
                    #print(f"pop: {stack_indent.pop()}")
                    stack.pop()
      head = stack_indent.get_top()
      if aft != head:
          #print(f"head: {head}")
          blank = head * ' '
          # 適切な行頭空白文字を付加
          str_line = blank+str_line.strip()
      
      if str_line.endswith(':'):
          #print(f"先読み:{str_line}")
          #printlst_cp[row_no])
          stack_indent.push(head + INDENT_NUM)
          # 1つ先読み
          try:
            stack.push(re.match(r" *", lst_cp[row_no]).end())
          except Exception:
            pass
      ##printstack_indent.stack)
      ##printstack.stack)
      lst_after.append(str_line)
      bef = aft
  ##printlst_after)
  return lst_after


# 走査: 関数とクラスの整形
def scan_format_method_class(lst, op_format):
  def_blank_num = 0
  class_blank_num = 0

  if not op_format['action']:
    return {
      'lst': lst,
      'def-blank': def_blank_num,
      'class-blank': class_blank_num
    }
  lst_cp = []
  for row_no, line in enumerate(lst, 1):
    str_line = line

    # 先頭の空白文字を取得
    blank_str = re.match(r" *", line).end() * ' '

    # 1行づつ正規表現にかける

    # 関数: 戻り値パターン -> 通常パターン
    sub_paterns_back = re.findall(REJEX_METHOD_NAME_BACK, line)
    if sub_paterns_back:
      # 括弧の中の考慮
      ##printsub_paterns_back[0])
      for i, elem in enumerate(sub_paterns_back[0]):
        if (i == 0 or i == 4 or i == 5) and elem != ' ':
          def_blank_num += 1
        elif (i == 2 or i == 7) and elem != '':
          def_blank_num += 1
      args = make_args(sub_paterns_back[0][3])
      str_line = blank_str + "def " + sub_paterns_back[0][1] + "(" + args + ") -> "\
            + sub_paterns_back[0][6] + ":"
    else:
      sub_paterns = re.findall(REJEX_METHOD_NAME, line)
      # 括弧の中の考慮
      if sub_paterns:
        for i, elem in enumerate(sub_paterns[0]):
          if i == 0 and elem != ' ':
            def_blank_num += 1
          elif (i == 2 or i == 4) and elem != '':
            def_blank_num += 1
        args = make_args(sub_paterns[0][3])
        str_line = blank_str + "def " + sub_paterns[0][1] + "(" + args + "):"

    # class
    sub_paterns_class = re.findall(REJEX_CLASS_NAME, line)
    if sub_paterns_class:
      #print(sub_paterns_class[0])
      if not sub_paterns_class[0][3].startswith('('):
        # ()がないパターン
        for i, elem in enumerate(sub_paterns_class[0]):
          if i == 0 and elem != ' ':
            class_blank_num += 1
          elif i == 2 and elem != '':
            class_blank_num += 1
        str_line = blank_str + "class " + sub_paterns_class[0][1] + ":"
      else:
        for i, elem in enumerate(sub_paterns_class[0]):
          if i == 0 and elem != ' ':
            class_blank_num += 1
          elif (i == 2 or i == 5) and elem != '':
            class_blank_num += 1
        args = make_args(sub_paterns_class[0][4])
        str_line = blank_str + "class " + sub_paterns_class[0][1] + "(" + args + "):"
    lst_cp.append(str_line)
  #print(f"def-blank:{def_blank_num}箇所")
  #print(f"class-blank:{class_blank_num}箇所")
  return {
    'lst': lst_cp,
    'def-blank': def_blank_num,
    'class-blank': class_blank_num
  }

# 命名規則クラス
class Naming():
  def __init__(self, op_naming_case) -> None:
      self.snake_flag = op_naming_case['snake']
      self.capwords_flag = op_naming_case['CapWords']
  
  def get_snake_flag(self):
    return self.snake_flag
  
  def get_capwords_flag(self):
    return self.capwords_flag


class ClassNaming(Naming):
  class_lst = []

  def __init__(self, op_naming) -> None:
    super().__init__(op_naming['class_case'])
  
  def check_lst(self, lst):
    lst_cp = []
    for line in lst:
      # 関数: 1行づつ正規表現にかける
      sub_paterns = re.findall(REJEX_CLASS_NAME, line)
      if sub_paterns:
        hit_class = sub_paterns[0][1]
        self.class_lst = hit_class
        # 行頭のインデントを取得
        starts_blank = re.match(r" *", line).end() * ' '
        
        if self.get_capwords_flag() and self.get_snake_flag():
          # '_'と大文字が両方入っていたらおかしい
          if '_' in hit_class and re.search(r'[A-Z]+', hit_class):
            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_CLASS_ALL)
        elif self.get_capwords_flag():
          # '_'が入っていたらおかしい
          if '_' in hit_class:
            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_CLASS_CAPWORDS)
        elif self.get_snake_flag():
          # 大文字が入っていたらおかしい
          if re.search(r'[A-Z]+', hit_class):
            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_CLASS_SNAKE)

      lst_cp.append(line)
    # 命名規則のlintがOFFの場合
    if not self.get_capwords_flag and not self.get_snake_flag:
      return lst
    return lst_cp

class MethodNaming(Naming):
  method_lst = []

  def __init__(self, op_naming) -> None:
    super().__init__(op_naming['method_case'])
  
  def check_lst(self, lst):
    lst_cp = []
    for line in lst:
      # 関数: 1行づつ正規表現にかける
      sub_paterns = re.findall(REJEX_METHOD_NAME, line)
      if sub_paterns:
        method = sub_paterns[0][1]
        self.method_lst.append(method)
        # 行頭のインデントを取得
        starts_blank = re.match(r" *", line).end() * ' '
        
        if self.get_capwords_flag() and self.get_snake_flag():
          # '_'と大文字が両方入っていたらおかしい
          if '_' in method and re.search(r'[A-Z]+', method):
            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_METHOD_ALL)
        elif self.get_capwords_flag():
          # '_'が入っていたらおかしい
          if '_' in method:
            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_METHOD_CAPWORDS)
        elif self.get_snake_flag():
          # 大文字が入っていたらおかしい
          if re.search(r'[A-Z]+', method):
            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_METHOD_SNAKE)
    
      lst_cp.append(line)
    
    # 命名規則のlintがOFFの場合
    if not self.get_capwords_flag and not self.get_snake_flag:
      return lst
    return lst_cp

class ValueNaming(Naming):
  value_lst = []

  def __init__(self, op_naming) -> None:
    super().__init__(op_naming['value_case'])
  
  def check_lst(self, lst):
    # 命名規則のlintがOFFの場合
    if not self.get_capwords_flag and not self.get_snake_flag:
      return lst
    
    #print(lst)
    # 関数とクラスを削除する正規表現
    STR_REJEX = REJEX_METHOD_NAME + '|' + REJEX_CLASS_NAME + '|' + REJEX_METHOD_NAME_BACK + '|'
    # 文字列を消去する正規表現
    STR_REJEX += REJEX_STRING_SINGLE + '|' + REJEX_STRING_DOUBLE + '|' + REJEX_COMMENT
    split_word = '\+|-|\*|\/|%|\*\*|=|\+=|-=|\*=|\/=|%=|\*\*=|==|!=|>|<|>=|<=|\\\\|\s|,|\[|\]|\{|\}|:'
    lst_cp = []
    already_lst = []
    for line in lst:
      #print(line)
      s = re.sub(STR_REJEX, '', line)
      words_lst = re.split(split_word, s)
      #print(words_lst)
      # 行頭のインデントを取得
      starts_blank = re.match(r" *", line).end() * ' '
      #print(words_lst)
      for word in words_lst:
        if word == '':
          pass
        elif word in RESERVED_WORDS:
          pass
        elif word in OTHER_WORDS:
          pass
        elif '(' in word or ')' in word or '.' in word:
          pass
        elif word.isdigit():
          pass
        elif word in already_lst:
          pass
        # 命名規則のチェック
        elif word:
          #printword)
          TRIM_WARNING_NAMING_VALUE_ALL = f"#[trim] Warning: 変数{word}: 大文字とアンダーバーを同時に含められません.\n"
          TRIM_WARNING_NAMING_VALUE_CAPWORDS = f"#[trim] Warning: 変数{word}: アンダーバーを含められません.\n"
          TRIM_WARNING_NAMING_VALUE_SNAKE = f"#[trim] Warning: 変数{word}: 大文字を含められません.\n"
          # 定数は例外
          if re.search('^[A-Z_]+$', word):
            #print"定数")
            pass
          elif self.get_capwords_flag() and self.get_snake_flag():
            # '_'と大文字が両方入っていたらおかしい
            if '_' in word and re.search(r'[A-Z]+', word):
              lst_cp.append(starts_blank + TRIM_WARNING_NAMING_VALUE_ALL)
          elif self.get_capwords_flag():
            # '_'が入っていたらおかしい
            if '_' in word:
              lst_cp.append(starts_blank + TRIM_WARNING_NAMING_VALUE_CAPWORDS)
          elif self.get_snake_flag():
            # 大文字が入っていたらおかしい
            if re.search(r'[A-Z]+', word):
              lst_cp.append(starts_blank + TRIM_WARNING_NAMING_VALUE_SNAKE)
          already_lst.append(word)
      lst_cp.append(line)
      
    return lst_cp


# 走査: 関数とクラスの命名規則チェック
def scan_naming_method_class(lst, op_naming):
  class_naming = ClassNaming(op_naming)
  method_naming = MethodNaming(op_naming)

  # 関数に関して
  lst = method_naming.check_lst(lst)

  # クラスに関して
  lst = class_naming.check_lst(lst)
    
  return {
    'lst': lst,
    'method_naming': method_naming,
    'class_naming': class_naming
  }


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
    starts_blank = re.match(r" *", line).end() * ' '
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

# 1行ごと変数の解析
def scan_naming_value(lst, op_naming):
  value_naming = ValueNaming(op_naming)

  # 変数に関して
  lst = value_naming.check_lst(lst)
    
  return lst


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
        s = re.match(r" *", line).end() * ' '
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
	stack_blank = MyStack()
	stack_start_line = MyStack()

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

# 3groupに分割 + アルファベット順にソート
def group_sort_import(lines, op_import):
    if not (op_import['sorting'] or op_import['grouping']):
      return lines
    
    # 3groupに分割 + アルファベット順にソート
    import_group1 = []
    import_group2 = []
    import_group3 = []

    import_lines = [line for line in lines if (line.startswith('import'))]
    from_lines = [line for line in lines if (line.startswith('from'))]
    not_import_lines = [line for line in lines if not ((line.startswith('import')) or (line.startswith('from')))]

    # 198個のpython 標準ライブラリ
    standard_lib = ['string',
    're',
    'difflib',
    'textwrap',
    'unicodedata',
    'stringprep',
    'readline',
    'rlcompleter',
    'struct',
    'codecs',
    'datetime',
    'zoneinfo',
    'calendar',
    'collections',
    'heapq',
    'bisect',
    'array',
    'weakref',
    'types',
    'copy',
    'pprint',
    'reprlib',
    'enum',
    'graphlib',
    'numbers',
    'math',
    'cmath',
    'decimal',
    'fractions',
    'random',
    'statistics',
    'itertools',
    'functools',
    'operator',
    'pathlib',
    'os',
    'fileinput',
    'stat',
    'filecmp',
    'tempfile',
    'glob',
    'fnmatch',
    'linecache',
    'shutil',
    'pickle',
    'copyreg',
    'shelve',
    'marshal',
    'dbm',
    'sqlite',
    'zlib',
    'gzip',
    'bz',
    'lzma',
    'zipfile',
    'tarfile',
    'csv',
    'configparser',
    'netrc',
    'xdrlib',
    'plistlib',
    'hashlib',
    'hmac',
    'secrets',
    'io',
    'time',
    'argparse',
    'getopt',
    'logging',
    'getpass',
    'curses',
    'platform',
    'errno',
    'ctypes',
    'threading',
    'multiprocessing',
    'concurrent',
    'subprocess',
    'sched',
    'queue',
    'contextvars',
    'asyncio',
    'socket',
    'ssl',
    'select',
    'selectors',
    'asyncore',
    'asynchat',
    'signal',
    'mmap',
    'email',
    'json',
    'mailcap',
    'mailbox',
    'mimetypes',
    'base',
    'binhex',
    'binascii',
    'quopri',
    'uu',
    'html',
    'xml',
    'webbrowser',
    'cgi',
    'cgitb',
    'wsgiref',
    'urllib',
    'http',
    'ftplib',
    'poplib',
    'imaplib',
    'nntplib',
    'smtplib',
    'smtpd',
    'telnetlib',
    'uuid',
    'socketserver',
    'xmlrpc',
    'ipaddress',
    'audioop',
    'aifc',
    'sunau',
    'wave',
    'chunk',
    'colorsys',
    'imghdr',
    'sndhdr',
    'ossaudiodev',
    'gettext',
    'locale',
    'turtle',
    'cmd',
    'shlex',
    'tkinter',
    'typing',
    'pydoc',
    'doctest',
    'unittest',
    'test',
    'bdb',
    'faulthandler',
    'pdb',
    'timeit',
    'trace',
    'tracemalloc',
    'distutils',
    'ensurepip',
    'venv',
    'zipapp',
    'sys',
    'sysconfig',
    'builtins',
    'warnings',
    'dataclasses',
    'contextlib',
    'abc',
    'atexit',
    'traceback',
    'gc',
    'inspect',
    'site',
    'code',
    'codeop',
    'zipimport',
    'pkgutil',
    'modulefinder',
    'runpy',
    'importlib',
    'ast',
    'symtable',
    'token',
    'keyword',
    'tokenize',
    'tabnanny',
    'pyclbr',
    'py',
    'compileall',
    'dis',
    'pickletools',
    'msilib',
    'msvcrt',
    'winreg',
    'winsound',
    'posix',
    'pwd',
    'spwd',
    'grp',
    'crypt',
    'termios',
    'tty',
    'pty',
    'fcntl',
    'pipes',
    'resource',
    'nis',
    'syslog',
    'optparse',
    'imp']

    base_url = 'https://pypi.org/project/'

    for line in import_lines:
      lib = re.sub('import ([a-z_]*)(\.)*.*','\\1',line)
      url = base_url + lib
      res = requests.get(url)
      #print(res)
      # lib = re.match('import (\w)* | from (\w)*',line)
      #print(lib)
      # 標準ライブラリの判別
      if lib in standard_lib:  
          import_group1.append(line)

      # third_party ライブラリの判別
      elif res.status_code == 200:
          import_group2.append(line)

      #その他のライブラリ
      else:
          import_group3.append(line)
    
    for line in from_lines:
      lib = re.sub('from ([a-z_]*)(\.)*.*','\\1',line)
      url = base_url + lib
      res = requests.get(url)
      #print(res)
      # lib = re.match('import (\w)* | from (\w)*',line)
      #print(lib)
      # 標準ライブラリの判別
      if lib in standard_lib:  
          import_group1.append(line)

      # third_party ライブラリの判別
      elif res.status_code == 200:
          import_group2.append(line)

      #その他のライブラリ
      else:
          import_group3.append(line)
      
    import_from_lines = sorted(import_group1) + [''] + sorted(import_group2) + [''] + sorted(import_group3) + ['']
    sorted_lines = import_from_lines + not_import_lines

    #print(import_group1)
    #print(import_group2)
    #print(import_group3)
    #print(sorted_lines)

    return sorted_lines

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
    op = body_dict['op']
    ##print(body_dict)

    # 空行をきれいにする
    lst_cp1 = list(map(lambda x: x.strip() if x.strip() == '' else x, body_dict['code_lst']))

    # compileが通るか確認
    lst_cp = list(map(lambda x: x + '\n' if not x.endswith('\n') else x , lst_cp1))
    compile_dic = is_comile_to_dic(lst_cp)
    if not compile_dic['flag']:
      #print(compile_dic['error'])
      return {
        'statusCode': 200,
        'body': json.dumps({
            'code_lst': compile_dic['error']
          })
      }
    
    lst_cp = group_sort_import(lst_cp, op['import_check'])
    lst_cp = scan_indent_config(lst_cp, op['style_check']['indent'])
    lst_dic = scan_format_method_class(lst_cp, op['style_check']['blank_format'])
    lst_cp = lst_dic['lst']
    def_blank_num = lst_dic['def-blank']
    class_blank_num = lst_dic['class-blank']
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
    #print(lst_cp)
    # 変数の解析
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

    f = open('myfile.py', 'w') 
    f.writelines(lst_cp)
    f.close()

    # TODO implement
    #return {
    #  'statusCode': 200,
    #  'body': json.dumps({
    #      'code_lst': lst_cp
    #    })
    #}
    return lst_cp


fileobj = open("def_sample_success.py", "r", encoding="utf_8")
lst = []
while True:
  line = fileobj.readline()
  if line:
      lst.append(line)
  else:
      break

json = {
    "body": {
      "code_lst": lst,
      "op": {
        'style_check': {
          # classや関数、演算子前後のフォーマット
          'blank_format': {
            'action': True, # 強くTrueを推奨
          },
          # indent設定
          'indent': {
            'type': ' ', 
            'num': 4,
            'tab_num': 4
          },
          # 1行あたりの文字数
          'count_word': {
            'action': True,
            'length': 90
          },
          # 行間
          'line_space': {
            'class_or_global_func': {
              'action': True,
            },
            'method': {
              'action': True,
            }
          }
        },
        'naming_check': {
          'class_case': {
            'snake': False,
            'CapWords': True
          },
          'method_case': {
            'snake': True,
            'CapWords': False
          },
          'value_case': {
            'snake': True,
            'CapWords': True
          }
        },
        'import_check': {
          'grouping': True,
          'sorting': True
        }
      }
    }
}

"""
以下どちらかを必ず選択
'indent': {
          'type': '\t', 
          'tab_num': 4
        }

'indent': {
          'type': ' ', 
          'num': 4,
          'tab_num': 4
        }
"""

lambda_handler(json, None)

