# 行末の演算子を除いた文字列と 行末の演算子を抽出
def find_lastchar(line):
    if (len(line)>= 6) and (line[-6:] in ["not in", "is not"]):
              return line[:-6], line[-6:]
    elif (len(line)>= 3) and (line[-3:] in ["and", "not"]):
        return line[:-3], line[-3:]
    elif line[-2:] in ["+=", "-=", "==", "!=", "<=", ">=", "<>","or", "is", "in"]:
        return line[:-2], line[-2:]
    elif line[-1:] in ["+", "-", "*", '/',"=","%"]:
        return line[:-1], line[-1:]
    else :
        return line, ""