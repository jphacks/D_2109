import traceback


# compileが通るか確認
def is_comile_to_dic(code_lst: list) -> dict:
  try:
    line = ''.join(code_lst)
    compile(line, '', 'exec')
    return {'flag': True}
  except Exception as e:
      return {'flag': False, 'error': str(traceback.format_exc())}
