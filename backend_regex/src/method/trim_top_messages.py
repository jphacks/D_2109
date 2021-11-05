from method.general import get_indent
from constants import TRIM_INFO_STYLE_BLANK_FALSE

# 命名規則のflagに合わせて設定表記用の文字列を生成
def make_naming_ops(flag_snake, flag_cap):
  ss = ' '
  if not (flag_snake or flag_cap):
    ss += "False"
  if flag_cap:
    ss += "CapWords"
  if flag_snake:
    s = '/' if flag_cap else '' 
    ss += s + "snake"
  return ss


# 整形後の上部に表示するメッセージを作成する
def trim_top_messages(lst_cp: list, 
                      op_style: dict, op_import: dict, op_naming: dict, 
                      def_blank_num: int, class_blank_num: int, 
                      s_warn_count: int):
    
    # インデント文字を取得
    indent = indent = get_indent(op_style['indent']['type'], op_style['indent']['num'])
    
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
        flag = op_style['blank_format']['action']
        elem += f"\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        if not flag:
          INFO_MES_LIST_CP.append(indent * 2 + TRIM_INFO_STYLE_BLANK_FALSE + '\n')
          i+=2
        continue
      if elem.startswith(indent + '・行あたりの文字数設定'):
        flag = op_style['count_word']['action']
        if flag:
          elem += f"{op_style['count_word']['length']}文字\n"
        else:
           elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent + '・クラス・グローバル関数間の間隔'):
        flag = op_style['line_space']['class_or_global_func']
        if flag:
          elem += f"2文字\n"
        else:
          elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent + '・メソッド間の間隔'):
        flag = op_style['line_space']['method']
        if flag:
          elem += f"1文字\n"
        else:
          elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent*2 + '・グルーピング'):
        flag = op_import['grouping']
        elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent*2 + '・アルファベットソート'):
        flag = op_import['sorting']
        elem += f"{flag}\n"
        INFO_MES_LIST_CP.append(elem)
        i+=1
        continue
      if elem.startswith(indent + '・命名規則'):
        INFO_MES_LIST_CP.append(elem + '\n')
        class_snake_flag = op_naming['class_case']['snake']
        method_snake_flag = op_naming['method_case']['snake']
        value_snake_flag = op_naming['value_case']['snake']
        class_cap_flag = op_naming['class_case']['CapWords']
        method_cap_flag = op_naming['method_case']['CapWords']
        value_cap_flag = op_naming['value_case']['CapWords']
        
        ss_class = make_naming_ops(class_snake_flag, class_cap_flag)
        ss_method = make_naming_ops(method_snake_flag, method_cap_flag)
        ss_value = make_naming_ops(value_snake_flag, value_cap_flag)
        
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
    return INFO_MES_LIST_CP