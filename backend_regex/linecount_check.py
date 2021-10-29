# 1行ごとに 文字数カウント 80文字以上のものは改行
def check_str_count(line: str):
    if len(line) >= 80:
        new_line = f'{line[:80]}\\\n'
        new_line += check_str_count(line[80:])
        return new_line
    else:
        return line
