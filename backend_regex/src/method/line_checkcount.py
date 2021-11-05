import re
from method.general import get_start_blank


# 1行ごとに 文字数カウント
def check_str_count(line:str) -> str:
  if len(line)>=80:
    new_line = f'{line[:80]}\\\n'
    new_line += check_str_count(line[80:])
    return new_line
  else:
    return line


# 1行ごとに 文字数カウント
def scan_style_count_word(lst: list, op_count_word: dict) -> dict:
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

