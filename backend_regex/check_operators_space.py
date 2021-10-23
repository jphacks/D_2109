# 行ごとに実行 : 指定した演算子
def check_operators_space(line:str):
  line = re.sub('(<>|<=|>=|is not|not in|-=|==|\+=|!=|=|\+|-|/|%|<|>|and|or|not|in|is)',' \\1 ',line)
  line = line.replace("  "," ")
  return line