import json
import re
import traceback
import keyword

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

RESERVED_WORDS = keyword.kwlist
OTHER_WORDS = ['Exception']

# 括弧の中を整形
def make_args(s_lst):
  #print(s_lst)
  s_lst = re.sub('[\s]', '', s_lst)
  lst = re.split(',', s_lst)
  args = ''
  for i, s in enumerate(lst):
    if i == 0:
      args += s
      continue
    args += ', ' + s
  return args


# スタックの定義
class MyStack:
    def __init__(self, n):
        self.stack = [0]
    def get_top(self):
      return self.stack[-1]
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
      return {'flag': False, 'error': str(traceback.print_exc())}

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

  
  stack = MyStack(0)

  lst_after = []

  top_strip_nums = [0]
  
  # 行頭に空白がある特殊パターンに対応
  lst_cp[0] = lst_cp[0].strip()

  block_indent_stack = MyStack(0)
  flag = False
  for row_no, line in enumerate(lst_cp, 1):
    # 空白文字のみの行の考慮
    if line.strip() == '':
      top_strip_nums.append(top_strip_nums[-1])
    else:
      top_strip_nums.append(re.match(' *', line).end())
    #print(line)
    #print(f"indent: {top_strip_nums[-1]}")

    # blockのindentをstackに格納
    if flag:
      block_indent = top_strip_nums[-1] -  top_strip_nums[-2]
      block_indent_stack.push(block_indent)
      flag = False
    # ブロックの終わりを検知
    #print(f"前: {top_strip_nums[-2]}")
    #print(f"今回: {top_strip_nums[-1]}")
    
    if row_no != 1 and top_strip_nums[-1] < top_strip_nums[-2] and line.strip()  != '':
      # indent数の差に合わせてpop(indent数の差/INDENT_NUM)
      #print(f"indent差分: {top_strip_nums[-2] - top_strip_nums[-1]}")
      #print(block_indent_stack.get_top())
      #print(f"INDENT_NUM: {INDENT_NUM}")
      #print(((top_strip_nums[-2] - top_strip_nums[-1])-block_indent_stack.get_top())//INDENT_NUM+1)

      for i in range(((top_strip_nums[-2] - top_strip_nums[-1])-block_indent_stack.get_top())//INDENT_NUM+1):
        stack.pop()
        block_indent_stack.pop()
        #print("stack_pop")
        #print(stack.stack)
    # ブロックの空白行頭数と比較
    if stack.get_top() != top_strip_nums[-1]:
        #print(f"正: {stack.get_top()}")
        #print(line)
        str = ' ' * stack.get_top() + line.strip()
        lst_after.append(str)
    else:
        lst_after.append(line)
    # classや関数などブロックの代わり目でindentを深くする
    if line.endswith(':'):
      flag = True
      stack.push(stack.get_top()+INDENT_NUM)
      #print("stack_push")
      #print("str:\n")
      #print(lst_after[-1])
      #print(stack.stack)
    
  #print(lst_after)
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
    str = line

    # 先頭の空白文字を取得
    blank_str = re.match(r" *", line).end() * ' '

    # 1行づつ正規表現にかける

    # 関数: 戻り値パターン -> 通常パターン
    sub_paterns_back = re.findall(REJEX_METHOD_NAME_BACK, line)
    if sub_paterns_back:
      # 括弧の中の考慮
      #print(str)
      #print(sub_paterns_back[0])
      for i, elem in enumerate(sub_paterns_back[0]):
        if (i == 0 or i == 4 or i == 5) and elem != ' ':
          def_blank_num += 1
        elif (i == 2 or i == 7) and elem != '':
          def_blank_num += 1
      args = make_args(sub_paterns_back[0][3])
      str = blank_str + "def " + sub_paterns_back[0][1] + "(" + args + ") -> "\
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
        str = blank_str + "def " + sub_paterns[0][1] + "(" + args + "):"

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
        str = blank_str + "class " + sub_paterns_class[0][1] + ":"
      else:
        for i, elem in enumerate(sub_paterns_class[0]):
          if i == 0 and elem != ' ':
            class_blank_num += 1
          elif (i == 2 or i == 5) and elem != '':
            class_blank_num += 1
        args = make_args(sub_paterns_class[0][4])
        str = blank_str + "class " + sub_paterns_class[0][1] + "(" + args + "):"
    lst_cp.append(str)
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
  def __init__(self, op_naming) -> None:
    super().__init__(op_naming['class_case'])
  
  def check_lst(self, lst):
    # 命名規則のlintがOFFの場合
    if not self.get_capwords_flag and not self.get_snake_flag:
      return lst
    
    lst_cp = []
    for line in lst:
      # 関数: 1行づつ正規表現にかける
      sub_paterns = re.findall(REJEX_CLASS_NAME, line)
      if sub_paterns:
        hit_class = sub_paterns[0][1]
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
    return lst_cp

class MethodNaming(Naming):
  def __init__(self, op_naming) -> None:
    super().__init__(op_naming['method_case'])
  
  def check_lst(self, lst):
    # 命名規則のlintがOFFの場合
    if not self.get_capwords_flag and not self.get_snake_flag:
      return lst
  
    lst_cp = []
    for line in lst:
      # 関数: 1行づつ正規表現にかける
      sub_paterns = re.findall(REJEX_METHOD_NAME, line)
      if sub_paterns:
        method = sub_paterns[0][1]
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
    return lst_cp

class ValueNaming(Naming):
  value_lst = []

  def __init__(self, op_naming) -> None:
    super().__init__(op_naming['value_case'])
  
  def check_lst(self, lst):
    # 命名規則のlintがOFFの場合
    if not self.get_capwords_flag and not self.get_snake_flag:
      return lst
    
    # 関数とクラスを削除する正規表現
    STR_REJEX = REJEX_METHOD_NAME + '|' + REJEX_CLASS_NAME + '|' + REJEX_METHOD_NAME_BACK + '|'
    # 文字列を消去する正規表現
    STR_REJEX += REJEX_STRING_SINGLE + '|' + REJEX_STRING_DOUBLE + '|' + REJEX_COMMENT
    split_word = '\+|-|\*|\/|%|\*\*|=|\+=|-=|\*=|\/=|%=|\*\*=|==|!=|>|<|>=|<=|\\\\|\s|,'
    lst_cp = []
    already_lst = []
    for line in lst:
      s = re.sub(STR_REJEX, '', line)
      words_lst = re.split(split_word, s)
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
          print(word)
          TRIM_WARNING_NAMING_VALUE_ALL = f"#[trim] Warning: 変数{word}: 大文字とアンダーバーを同時に含められません.\n"
          TRIM_WARNING_NAMING_VALUE_CAPWORDS = f"#[trim] Warning: 変数{word}: アンダーバーを含められません.\n"
          TRIM_WARNING_NAMING_VALUE_SNAKE = f"#[trim] Warning: 変数{word}: 大文字を含められません.\n"
          # 定数は例外
          if re.search('^[A-Z_]+$', word):
            print("aaaa")
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
    
  return lst


# 1行ごとに 文字数カウント
def scan_style_count_word(lst, op_count_word):
  s_warn_count = 0
  if not op_count_word['action']:
    return lst
  lst_cp = []
  #print("#######################")
  pattern = re.compile(r'^[^\\]*\\$')
  
  buffer = []
  for line in lst:
    #print(buffer)
    #print(line)
    match_flag = bool(pattern.match(line))
    # 行頭のインデントを取得
    starts_blank = re.match(r" *", line).end() * ' '
    # もし'/'で終わってたら状態を保存
    if match_flag:
      #print("match!!")
      buffer.append({'blank': starts_blank, 'mes': line})
    if len(line)>= op_count_word["length"] + 1 and (not match_flag):
      blank = starts_blank if len(buffer) == 0 else buffer[0]['blank']
      TRIM_WARNING_STYLE_COUNT_WARD = f'# [trim] Warning: 1行あたりの行数は最大{op_count_word["length"]}文字です.適切な位置で折り返してください.'
      lst_cp.append(blank + TRIM_WARNING_STYLE_COUNT_WARD)
      s_warn_count += 1
      for dic in buffer:
        lst_cp.append(dic['mes'])
      lst_cp.append(line)
      buffer = []
    # 状態の初期化
    if not match_flag and len(line)<81:
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



def lambda_handler(event, context):
    #body_dict = json.loads(event['body'])
    body_dict = event['body']
    op = body_dict['op']
    #print(body_dict)

    # compileが通るか確認
    compile_dic = is_comile_to_dic(body_dict['code_lst'])
    if not compile_dic['flag']:
      #print(compile_dic['error'])
      #return {
      #  'statusCode': 400,
      #  'body': json.dumps({
      #      'error': compile_dic['error']
      #    })
      #}
      return
    
    lst_cp = scan_indent_config(body_dict['code_lst'], op['style_check']['indent'])
    lst_dic = scan_format_method_class(lst_cp, op['style_check']['blank_format'])
    lst_cp = lst_dic['lst']
    def_blank_num = lst_dic['def-blank']
    class_blank_num = lst_dic['class-blank']
    lst_cp = scan_naming_method_class(lst_cp, op['naming_check'])
    

    # 空行をきれいにする
    lst_cp = list(map(lambda x: x.strip() if x.strip() == '' else x, lst_cp))
    # 文字数警告
    lst_dic = scan_style_count_word(lst_cp, op['style_check']['count_word'])
    lst_cp = lst_dic['lst']
    s_warn_count = lst_dic['s_warn_count']
    # 改行コードを追加
    lst_cp = list(map(lambda x: x + '\n', lst_cp))
    # 変数の解析
    lst_cp = scan_naming_value(lst_cp, op['naming_check'])
    # インデント文字
    indent = '\t' if op['style_check']['indent']['type'] == '\t' else ' '*op['style_check']['indent']['num']
    
    INFO_MES_LIST = [
      '"""©trim 整形実行後ファイル\n',
      indent + '・空白整形の文字数設定 - ',
      indent * 2 + f'関数: {def_blank_num}箇所\n',
      indent * 2 + f'クラス: {class_blank_num}箇所\n',
      indent + '・行あたりの文字数設定 - ',
      indent * 2 + f'[警告] {s_warn_count}箇所\n',
      '"""\n\n',
    ]
    # 上からopに応じて変形し、=> INFO_MES_LIST_CPへ => lst_cpに戻す
    INFO_MES_LIST_CP = []
    i = 0
    while True:
      elem = INFO_MES_LIST[i]
      #print(elem)
      if elem.startswith(indent + '・空白整形'):
        flag = op['style_check']['blank_format']['action']
        elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        if not flag:
          INFO_MES_LIST_CP.append(indent * 2 + TRIM_INFO_STYLE_BLANK_FALSE + '\n')
          i+=2
        continue
      if elem.startswith(indent + '・行あたりの文字数設定'):
        flag = op['style_check']['count_word']['action']
        elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
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
        
    #print(lst_cp)
    
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


fileobj = open("def_sample.py", "r", encoding="utf_8")
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
            'length': 120
          },
          # 行間
          'line_space': {
            'class': {
              'action': True,
              'len': 2
            },
            'global_method': {
              'action': True,
              'len': 2
            },
            'class_method': {
              'action': True,
              'len': 1
            }
          }
        },
        'naming_check': {
          'class_case': {
            'snake': True,
            'CapWords': False
          },
          'method_case': {
            'snake': True,
            'CapWords': False
          },
          'value_case': {
            'snake': True,
            'CapWords': False
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

