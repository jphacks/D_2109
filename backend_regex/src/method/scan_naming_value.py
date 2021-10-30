import re
import keyword

REJEX_METHOD_NAME = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*):"
REJEX_METHOD_NAME_BACK = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*)->([ |\t]*)(\w+)([ |\t]*):"
REJEX_CLASS_NAME = "class([ |\t]*)(\w+)([ |\t]*)(\((.*)\))*([ |\t]*):"

REJEX_STRING_DOUBLE = "\s*\".*\"\s*"
REJEX_STRING_SINGLE = "\s*\'.*\'\s*"
REJEX_COMMENT = "\s*#.*\s*\n\s*"

RESERVED_WORDS = keyword.kwlist
OTHER_WORDS = ['Exception']

# 命名規則クラス
class Naming():
  def __init__(self, op_naming_case) -> None:
      self.snake_flag = op_naming_case['snake']
      self.capwords_flag = op_naming_case['CapWords']
  
  def get_snake_flag(self):
    return self.snake_flag
  
  def get_capwords_flag(self):
    return self.capwords_flag

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


# 1行ごと変数の解析
def scan_naming_value(lst, op_naming):
  value_naming = ValueNaming(op_naming)

  # 変数に関して
  lst = value_naming.check_lst(lst)
    
  return lst