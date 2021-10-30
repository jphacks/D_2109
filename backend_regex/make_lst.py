fileobj = open("def_sample.py", "r", encoding="utf_8")
lst = []
while True:
  line = fileobj.readline()
  if line:
      lst.append(line)
  else:
      break

print(lst)

