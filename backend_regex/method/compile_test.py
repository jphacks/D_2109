import traceback


fileobj = open("def_sample.py", "r", encoding="utf_8")
lst = []
line = ''.join(fileobj.readlines())

try:
    compiled = compile(line, '', 'exec')
except Exception as e:
    error = traceback.print_exc()
    print(str(error))
