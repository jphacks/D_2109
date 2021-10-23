# 1行に1つのimport文になるように分割
def split_import(line: str):
    # 1つのみのimportはそのまま
    if len(line.split(',')) == 1:
        return line
    # 複数import の場合は、改行
    else:
        new_lines = line.split(',')[0]
        for import_name in line.split(',')[1:]:
            import_name = import_name.replace(' ', '')
            # new_lines += '\n'
            new_lines += f'\nimport {import_name}'
    return new_lines
