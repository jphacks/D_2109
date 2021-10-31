from method.general import get_start_blank_num

# 1行に1つのimport文になるように分割
def split_import(lst: list) -> list:
  lst_cp = []
  for line in lst:
    # 行頭のインデントを取得
    starts_blank = get_start_blank_num(line)
    strip_line = line.strip()
    if strip_line.startswith('import'):
      # 1つのみのimportはそのまま
      if len(strip_line.split(',')) == 1:
        lst_cp.append(line)
      # 複数import の場合は、改行
      else:
        new_lines = strip_line.split(',')
        for import_name in new_lines:
          if import_name.startswith('import'):
            import_name = import_name.replace('import', '')
          import_name = import_name.replace(' ','')
          lst_cp.append(starts_blank + f"import {import_name}\n")
    else:
      lst_cp.append(line)
  return lst_cp