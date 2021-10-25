# -*- coding: utf-8 -*-

import json
import urllib.request

POST_URL = 'https://d1cg4t8u2gajxa.cloudfront.net/api-v1/pyformat'
HEADERS = {
    'Content-Type': 'application/json',
}
fileobj = open("def_sample.py", "r", encoding="utf_8")

lst = []
while True:
    line = fileobj.readline()
    if line:
        lst.append(line)
    else:
        break

data = {
    'code_lst': lst,
}
print(lst)
exit()
req = urllib.request.Request(POST_URL, json.dumps(data).encode(), HEADERS)
try:
    with urllib.request.urlopen(req) as res:
        body = res.read()
except urllib.error.HTTPError as err:
    print(err.reason)
except urllib.error.URLError as err:
    print(err.reason)