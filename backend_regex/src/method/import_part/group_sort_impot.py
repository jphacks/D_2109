import re
import urllib.request
from method.general import get_start_blank_num
from constants import STANDARD_LIB, TRIM_INPORT_COMMENT

def group_import(lines):
    # 3groupに分割 (ソートなし)
    import_group1 = []
    import_group2 = []
    import_group3 = []

    import_lines = []
    from_lines = []
    not_import_lines = []
    for line in lines:
        if len(get_start_blank_num(line)) != 0:
            not_import_lines.append(line)
            continue
        if line.startswith('import'):
            import_lines.append(line)
            continue
        if line.startswith('from'):
            from_lines.append(line)
            continue
        if not (line.startswith('import') or line.startswith('from')):
            not_import_lines.append(line)

    base_url = 'https://pypi.org/project/'

    for line in import_lines:
        lib = re.sub('import ([a-z_]*)(\\.)*.*', '\\1', line)
        url = base_url + lib
        req = urllib.request.Request(url, method='GET')
        
        # 標準ライブラリの判別
        if lib.strip() in STANDARD_LIB:  
          import_group1.append(line)
          continue
              
        try:
          res = urllib.request.urlopen(req)
          # third_party ライブラリの判別
          import_group2.append(line)
        except Exception:
          #その他のライブラリ
          import_group3.append(line)

    for line in from_lines:
        lib = re.sub('from ([a-z_]*)(\\.)*.*', '\\1', line)
        url = base_url + lib
        req = urllib.request.Request(url, method='GET')
        
        # 標準ライブラリの判別
        if lib.strip() in STANDARD_LIB:  
          import_group1.append(line)
          continue
              
        try:
          res = urllib.request.urlopen(req)
          # third_party ライブラリの判別
          import_group2.append(line)
        except Exception:
          #その他のライブラリ
          import_group3.append(line)

    import_from_lines = import_group1 + [''] + import_group2 + [''] + import_group3 + ['']
    group_lines = import_from_lines + not_import_lines

    return group_lines


# 3groupに分割なし + アルファベット順にソート
def sort_import(lines):
  import_lines = []
  from_lines = []
  not_import_lines = []
  for line in lines:
    if len(get_start_blank_num(line)) != 0:
      not_import_lines.append(line)
      continue
    if line.startswith('import'):
      import_lines.append(line)
      continue
    if line.startswith('from'):
      from_lines.append(line)
      continue
    if not (line.startswith('import') or line.startswith('from')):
      not_import_lines.append(line)

  import_from_lines = sorted(from_lines) + sorted(import_lines) + ['']
  sorted_lines = import_from_lines + not_import_lines

  return sorted_lines
