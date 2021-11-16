import json

from method.is_comile_to_dic import is_comile_to_dic
from method.scan_indent_config import scan_indent_config
from method.naming import scan_naming_method_class, scan_naming_value
from method.import_part.split_import import split_import
from method.import_part.group_sort_impot import group_sort_import
from method.scan_format_method_class import scan_format_method_class
from method.line_checkcount import scan_style_count_word
from method.scan_operators_space import scan_operators_space
from method.blank_lines import blank_lines
from method.trim_top_messages import trim_top_messages
from method.general import strip_blank_line, add_newline_char, delete_blank_ends, replace_tab_to_blank, replace_blank_to_tab


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
    
    print(method_naming.method_lst)
    print(method_naming.method_hit_lst)

    # 1行辺りの文字数をチェック
    lst_dic = scan_style_count_word(lst_cp, op['style_check']['count_word'])
    lst_cp = lst_dic['lst']
    s_warn_count = lst_dic['s_warn_count']

    # 演算子前後の空白を調整
    lst_cp = scan_operators_space(lst_cp, method_naming, class_naming)
    
	  # 改行コードを追加
    lst_cp = add_newline_char(lst_cp)

    # 変数の解析と命名規則チェック
    lst_dic = scan_naming_value(lst_cp, op['naming_check'])
    lst_cp = lst_dic['lst']
    value_naming = lst_dic['value_naming']

	  # 整形後の上部に表示するメッセージを作成する
    lst_cp = trim_top_messages(
      lst_cp, 
      op['style_check'], 
      op['import_check'],
      op['naming_check'],
      def_blank_num,
      class_blank_num,
      s_warn_count, # 行辺りの文字数設定
	  )

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
with open('../../../rule.json') as json_data:
  op = json.load(json_data)
  # bodyを文字列として送る(POST通信を想定)
  event['body'] = json.dumps({
    'code_lst': lst,
    'op': op
  })
  lambda_handler((event), None)