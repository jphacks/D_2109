import json

from constants import TRIM_INFO_STYLE_BLANK_FALSE
from method.is_comile_to_dic import is_comile_to_dic
from method.scan_indent_config import scan_indent_config
from method.naming import scan_naming_method_class, scan_naming_value
from method.import_part.split_import import split_import
from method.import_part.group_sort_impot import group_sort_import
from method.scan_format_method_class import scan_format_method_class
from method.line_checkcount import scan_style_count_word
from method.scan_operators_space import scan_operators_space
from method.blank_lines import blank_lines
from method.general import strip_blank_line, add_newline_char, delete_blank_ends, replace_tab_to_blank, replace_blank_to_tab, get_indent


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
    body_dict = json.loads(event['body'])
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
    lst_cp = delete_blank_ends(lst_cp)

    # タブ文字を' '*INDENT_TAB_NUMに置き換え
    lst_cp = replace_tab_to_blank(lst_cp, INDENT_TAB_NUM)

    # import部のスプリット
    lst_cp = split_import(lst_cp)
    
    # import部のグルーピング・ソーティング
    lst_cp = group_sort_import(lst_cp, op['import_check'])

    # 走査して、適切なインデントに調節していく 
    lst_cp = scan_indent_config(lst_cp, op['style_check']['indent'])
    
    # 走査して、関数とクラスの整形を行う
    lst_dic = scan_format_method_class(lst_cp, op['style_check']['blank_format'])
    lst_cp = lst_dic['lst']
    def_blank_num = lst_dic['def-blank']
    class_blank_num = lst_dic['class-blank']
    
    # 走査して、関数とクラスの命名規則をチェックする
    lst_dic = scan_naming_method_class(lst_cp, op['naming_check'])
    lst_cp = lst_dic['lst']
    method_naming = lst_dic['method_naming']
    class_naming = lst_dic['class_naming']

    # 1行辺りの文字数をチェック
    lst_dic = scan_style_count_word(lst_cp, op['style_check']['count_word'])
    lst_cp = lst_dic['lst']
    s_warn_count = lst_dic['s_warn_count']

    # 演算子前後の空白を調整
    lst_cp = scan_operators_space(lst_cp, method_naming, class_naming)
    
    # 変数の解析と命名規則チェック
    lst_cp = scan_naming_value(lst_cp, op['naming_check'])

    # 改行コードを追加
    lst_cp = add_newline_char(lst_cp)

    # インデント文字を取得
    indent = get_indent(op['style_check']['indent']['type'], op['style_check']['indent']['num'])
    
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
    lst_cp = replace_blank_to_tab(lst_cp, op['style_check']['indent']['type'], op['style_check']['indent']['tab_num'])

    # 行間の調整
    lst_cp = blank_lines(lst_cp, op['style_check']['line_space'])

    f = open('output/output.py', 'w') 
    f.writelines(lst_cp)
    f.close()

    # TODO implement
    return {
      'statusCode': 200,
      'body': json.dumps({
          'code_lst': lst_cp
        })
    }

# ローカルのみ
fileobj = open("input/dirty_code.py", "r", encoding="utf_8")
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
  lambda_handler((event), None)