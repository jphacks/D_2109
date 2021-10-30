import re
import requests

# 198個のpython 標準ライブラリ
standard_lib = ['string',
                're',
                'difflib',
                'textwrap',
                'unicodedata',
                'stringprep',
                'readline',
                'rlcompleter',
                'struct',
                'codecs',
                'datetime',
                'zoneinfo',
                'calendar',
                'collections',
                'heapq',
                'bisect',
                'array',
                'weakref',
                'types',
                'copy',
                'pprint',
                'reprlib',
                'enum',
                'graphlib',
                'numbers',
                'math',
                'cmath',
                'decimal',
                'fractions',
                'random',
                'statistics',
                'itertools',
                'functools',
                'operator',
                'pathlib',
                'os',
                'fileinput',
                'stat',
                'filecmp',
                'tempfile',
                'glob',
                'fnmatch',
                'linecache',
                'shutil',
                'pickle',
                'copyreg',
                'shelve',
                'marshal',
                'dbm',
                'sqlite',
                'zlib',
                'gzip',
                'bz',
                'lzma',
                'zipfile',
                'tarfile',
                'csv',
                'configparser',
                'netrc',
                'xdrlib',
                'plistlib',
                'hashlib',
                'hmac',
                'secrets',
                'io',
                'time',
                'argparse',
                'getopt',
                'logging',
                'getpass',
                'curses',
                'platform',
                'errno',
                'ctypes',
                'threading',
                'multiprocessing',
                'concurrent',
                'subprocess',
                'sched',
                'queue',
                'contextvars',
                'asyncio',
                'socket',
                'ssl',
                'select',
                'selectors',
                'asyncore',
                'asynchat',
                'signal',
                'mmap',
                'email',
                'json',
                'mailcap',
                'mailbox',
                'mimetypes',
                'base',
                'binhex',
                'binascii',
                'quopri',
                'uu',
                'html',
                'xml',
                'webbrowser',
                'cgi',
                'cgitb',
                'wsgiref',
                'urllib',
                'http',
                'ftplib',
                'poplib',
                'imaplib',
                'nntplib',
                'smtplib',
                'smtpd',
                'telnetlib',
                'uuid',
                'socketserver',
                'xmlrpc',
                'ipaddress',
                'audioop',
                'aifc',
                'sunau',
                'wave',
                'chunk',
                'colorsys',
                'imghdr',
                'sndhdr',
                'ossaudiodev',
                'gettext',
                'locale',
                'turtle',
                'cmd',
                'shlex',
                'tkinter',
                'typing',
                'pydoc',
                'doctest',
                'unittest',
                'test',
                'bdb',
                'faulthandler',
                'pdb',
                'timeit',
                'trace',
                'tracemalloc',
                'distutils',
                'ensurepip',
                'venv',
                'zipapp',
                'sys',
                'sysconfig',
                'builtins',
                'warnings',
                'dataclasses',
                'contextlib',
                'abc',
                'atexit',
                'traceback',
                'gc',
                'inspect',
                'site',
                'code',
                'codeop',
                'zipimport',
                'pkgutil',
                'modulefinder',
                'runpy',
                'importlib',
                'ast',
                'symtable',
                'token',
                'keyword',
                'tokenize',
                'tabnanny',
                'pyclbr',
                'py',
                'compileall',
                'dis',
                'pickletools',
                'msilib',
                'msvcrt',
                'winreg',
                'winsound',
                'posix',
                'pwd',
                'spwd',
                'grp',
                'crypt',
                'termios',
                'tty',
                'pty',
                'fcntl',
                'pipes',
                'resource',
                'nis',
                'syslog',
                'optparse',
                'imp']

comment = ['# [trim] Info: グルーピング済みです',
           '# [trim] Info: アルファベットソート済みです'
          ]


def group_sort_import(lines):
    # 3groupに分割 + アルファベット順にソート
    import_group1 = []
    import_group2 = []
    import_group3 = []

    import_lines = [line for line in lines if (line.startswith('import'))]
    from_lines = [line for line in lines if (line.startswith('from'))]
    not_import_lines = [
        line for line in lines if not (
            (line.startswith('import')) or (
                line.startswith('from')))]

    base_url = 'https://pypi.org/project/'

    for line in import_lines:
        lib = re.sub('import ([a-z_]*)(\\.)*.*', '\\1', line)
        url = base_url + lib
        res = requests.get(url)
        print(res)
        # lib = re.match('import (\w)* | from (\w)*',line)
        print(lib)
        # 標準ライブラリの判別
        if lib in standard_lib:
            import_group1.append(line)

        # third_party ライブラリの判別
        elif res.status_code == 200:
            import_group2.append(line)

        # その他のライブラリ
        else:
            import_group3.append(line)

    for line in from_lines:
        lib = re.sub('from ([a-z_]*)(\\.)*.*', '\\1', line)
        url = base_url + lib
        res = requests.get(url)
        print(res)
        # lib = re.match('import (\w)* | from (\w)*',line)
        print(lib)
        # 標準ライブラリの判別
        if lib in standard_lib:
            import_group1.append(line)

        # third_party ライブラリの判別
        elif res.status_code == 200:
            import_group2.append(line)

        # その他のライブラリ
        else:
            import_group3.append(line)

    import_from_lines = sorted(
        import_group1) + [''] + sorted(import_group2) + [''] + sorted(import_group3) + ['']
    sorted_lines = comment + import_from_lines + not_import_lines

    print(import_group1)
    print(import_group2)
    print(import_group3)
    print(sorted_lines)

    return sorted_lines

def group_import(lines):
    # 3groupに分割 (ソートなし)
    import_group1 = []
    import_group2 = []
    import_group3 = []

    import_lines = [line for line in lines if (line.startswith('import'))]
    from_lines = [line for line in lines if (line.startswith('from'))]
    not_import_lines = [
        line for line in lines if not (
            (line.startswith('import')) or (
                line.startswith('from')))]

    base_url = 'https://pypi.org/project/'

    for line in import_lines:
        lib = re.sub('import ([a-z_]*)(\\.)*.*', '\\1', line)
        url = base_url + lib
        res = requests.get(url)
        print(res)
        # lib = re.match('import (\w)* | from (\w)*',line)
        print(lib)
        # 標準ライブラリの判別
        if lib in standard_lib:
            import_group1.append(line)

        # third_party ライブラリの判別
        elif res.status_code == 200:
            import_group2.append(line)

        # その他のライブラリ
        else:
            import_group3.append(line)

    for line in from_lines:
        lib = re.sub('from ([a-z_]*)(\\.)*.*', '\\1', line)
        url = base_url + lib
        res = requests.get(url)
        print(res)
        # lib = re.match('import (\w)* | from (\w)*',line)
        print(lib)
        # 標準ライブラリの判別
        if lib in standard_lib:
            import_group1.append(line)

        # third_party ライブラリの判別
        elif res.status_code == 200:
            import_group2.append(line)

        # その他のライブラリ
        else:
            import_group3.append(line)

    import_from_lines = import_group1 + [''] + import_group2 + [''] + import_group3 + ['']
    group_lines = comment + import_from_lines + not_import_lines

    return group_lines

def sort_import(lines):
    # 3groupに分割なし + アルファベット順にソート

    import_lines = [line for line in lines if (line.startswith('import'))]
    from_lines = [line for line in lines if (line.startswith('from'))]
    not_import_lines = [
        line for line in lines if not (
            (line.startswith('import')) or (
                line.startswith('from')))]

    import_from_lines = sorted(import_lines) + ['']
    sorted_lines = comment + import_from_lines + not_import_lines

    return sorted_lines
