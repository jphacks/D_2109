import json
import re

REJEX_METHOD_NAME = "def( |\t)+(\w+)( |\t)*\((.*)\)( |\t)*:"
REJEX_METHOD_NAME_BACK = "def( |\t)+(\w+)( |\t)*\((.*)\)( |\t)*->( |\t)*(\w+)( |\t)*:"
REJEX_CLASS_NAME = "class( |\t)+(\w+)( |\t)*(\((.*)\))*( |\t)*:"

# 括弧の中を整形
def make_args(s_lst):
  print(s_lst)
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
  #print(lst_cp)
  # indent typeの判定
  #if op_indent['type'] == ' ':
    # 
  #elif op_indent['type'] == '\t':

  
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
    print(line)
    print(f"indent: {top_strip_nums[-1]}")

    # blockのindentをstackに格納
    if flag:
      block_indent = top_strip_nums[-1] -  top_strip_nums[-2]
      block_indent_stack.push(block_indent)
      flag = False
    # ブロックの終わりを検知
    print(f"前: {top_strip_nums[-2]}")
    print(f"今回: {top_strip_nums[-1]}")
    
    if row_no != 1 and top_strip_nums[-1] < top_strip_nums[-2] and line.strip()  != '':
      # indent数の差に合わせてpop(indent数の差/INDENT_NUM)
      print(f"indent差分: {top_strip_nums[-2] - top_strip_nums[-1]}")
      print(block_indent_stack.get_top())
      #print(f"INDENT_NUM: {INDENT_NUM}")
      print(((top_strip_nums[-2] - top_strip_nums[-1])-block_indent_stack.get_top())//INDENT_NUM+1)

      for i in range(((top_strip_nums[-2] - top_strip_nums[-1])-block_indent_stack.get_top())//INDENT_NUM+1):
        stack.pop()
        block_indent_stack.pop()
        print("stack_pop")
        print(stack.stack)
    # ブロックの空白行頭数と比較
    if stack.get_top() != top_strip_nums[-1]:
        print(f"正: {stack.get_top()}")
        print(line)
        str = ' ' * stack.get_top() + line.strip()
        lst_after.append(str)
    else:
        lst_after.append(line)
    # classや関数などブロックの代わり目でindentを深くする
    if line.endswith(':'):
      flag = True
      stack.push(stack.get_top()+INDENT_NUM)
      print("stack_push")
      print("str:\n")
      print(lst_after[-1])
      print(stack.stack)
    
  print(lst_after)
  return lst_after


# 走査: 関数とクラスの整形
def scan_format_method_class(lst):
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
      args = make_args(sub_paterns_back[0][3])
      str = blank_str + "def " + sub_paterns_back[0][1] + "(" + args + ") -> "\
            + sub_paterns_back[0][6] + ":"
    else:
      sub_paterns = re.findall(REJEX_METHOD_NAME, line)
      # 括弧の中の考慮
      if sub_paterns:
        args = make_args(sub_paterns[0][3])
        str = blank_str + "def " + sub_paterns[0][1] + "(" + args + "):"

    # class
    sub_paterns_class = re.findall(REJEX_CLASS_NAME, line)
    if sub_paterns_class:
      #print(sub_paterns_class[0])
      if not sub_paterns_class[0][3].startswith('('):
        # ()がないパターン
        str = blank_str + "class " + sub_paterns_class[0][1] + ":"
      else:
        args = make_args(sub_paterns_class[0][4])
        str = blank_str + "class " + sub_paterns_class[0][1] + "(" + args + "):"
    lst_cp.append(str)
  return lst_cp

def lambda_handler(event, context):
    #body_dict = json.loads(event['body'])
    body_dict = event['body']
    op = body_dict['op']
    print(body_dict)
    lst_cp = scan_indent_config(body_dict['code_lst'], op['style_check']['indent'])
    lst_cp = scan_format_method_class(lst_cp)
    
    # 空行をきれいにする
    lst_cp = list(map(lambda x: x.strip() if x.strip() == '' else x, lst_cp))
    # 改行コードを追加
    lst_cp = list(map(lambda x: x + '\n', lst_cp))
    # タブ文字設定の場合は半角X個をタブ文字に変換
    if op['style_check']['indent']['type'] == '\t':
      lst_cp = list(map(lambda x: re.sub(' '*op['style_check']['indent']['tab_num'], '\t', x), lst_cp))
    
    print(lst_cp)
    
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

json = {
    "body": {
      "code_lst": [' a=3\n', 'v=2\n', '\n', 'def a():\n', '\tpass\n', '\n', '\n', 'def  \tadd_box        \t(a  \t, b, c = \t3) \t\t\t\t:       \t\n', '  ab = 2\n', '  a = 3\n', '  def aaaa():\n', '    return ab\n', '  return  ab\n', '\n', '\n', '\n', 'class     \tPermissionMixin   :\n', '\t  def __init__(self) -> None:\n', '\t\t  pass\n', '\t  def a(self):\n', '\t\t  pass\n', '\n', 'class BaseUser\t()  :\n', '\tdef __init__(self) -> None:\n', '\t\tpass\n', '\tpass\n', '\n', 'class User  (\t   BaseUser,  PermissionMixin\t):\n', '\tname = "aaaa"\n', '\n', '\tdef __init__(self) -> None:\n', '\t\tsuper().__init__()\n', '\n', '\tdef getName(self):\n', '\t\treturn self.name'],
      "op": {
        'style_check': {
          # classや関数、演算子前後のフォーマット
          'blank_format': {
            'action': True, # 強くTrueを推奨
          },
          # indent設定
          'indent': {
            'action': True,
            'type': '\t',
            'tab_num': 4
          },
          # 1行あたりの文字数
          'count_word': {
            'action': True,
            'length': 80
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
            'CapWords': True
          },
          'method_case': {
            'snake': True,
            'CapWords': True
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

