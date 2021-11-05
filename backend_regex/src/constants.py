import keyword

# 198個のpython 標準ライブラリ
STANDARD_LIB = [
  'string',
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
  'imp'
]

REJEX_METHOD_NAME = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*):"
REJEX_METHOD_NAME_BACK = "def([ |\t]+)(\w+)([ |\t]*)\((.*)\)([ |\t]*)->([ |\t]*)(\w+)([ |\t]*):"
REJEX_CLASS_NAME = "class([ |\t]*)(\w+)([ |\t]*)(\((.*)\))*([ |\t]*):"

REJEX_STRING_DOUBLE = "\s*\".*\"\s*"
REJEX_STRING_SINGLE = "\s*\'.*\'\s*"
REJEX_COMMENT = "\s*#.*\s*\n\s*"

REJEX_IMPORT = "\s*import\s+[\w\.\,\s]+"
REJEX_IMPORT_FROM = "\s*from\s+[\w\.]+\s*import\s+[\w\.\,\s]+"

TRIM_WARNING_NAMING_METHOD_ALL = "# [trim] Warning: 関数名に大文字とアンダーバーを同時に含められません."
TRIM_WARNING_NAMING_METHOD_SNAKE = "# [trim] Warning: 関数名に大文字は含められません."
TRIM_WARNING_NAMING_METHOD_CAPWORDS = "# [trim] Warning: 関数名にアンダーバーは含められません."

TRIM_WARNING_NAMING_CLASS_ALL = "# [trim] Warning: クラス名に大文字とアンダーバーを同時に含められません."
TRIM_WARNING_NAMING_CLASS_SNAKE = "# [trim] Warning: クラス名に大文字は含められません."
TRIM_WARNING_NAMING_CLASS_CAPWORDS = "# [trim] Warning: クラス名にアンダーバーは含められません."

TRIM_INFO_STYLE_BLANK_FALSE = "Info: PEP8に基づく、空白の整形設定を行う事を推奨します."
TRIM_INFO_STYLE_IMPORT_GROUP = "# [trim] Info: グルーピング済みです."
TRIM_INFO_STYLE_IMPORT_SORT = "# [trim] Info: アルファベットソート済みです."

TRIM_INPORT_COMMENT = [
  '# [trim] Info: グルーピング済みです',
  '# [trim] Info: アルファベットソート済みです'
]

RESERVED_WORDS = keyword.kwlist

# ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
#  'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for',
#  'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
#  'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

OTHER_WORDS = ['Exception']