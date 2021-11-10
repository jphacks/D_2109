import subprocess
import os
import datetime
import pathlib
import glob
import json

from method.is_comile_to_dic import is_comile_to_dic
from method.scan_indent_config import scan_indent_config
from method.naming import scan_naming_method_class, scan_naming_value
from method.import_part.split_import import split_import
from method.import_part.group_sort_impot import group_sort_import
from method.scan_format_method_class import scan_format_method_class
from method.line_checkcount import scan_style_count_word
from method.scan_operators_space import scan_operators_space
from method.blank_lines import blank_lines
from method.trim_top_messages import trim_top_messages
from method.general import strip_blank_line, add_newline_char, delete_blank_ends, replace_tab_to_blank, replace_blank_to_tab


# 実行パス(Linuxコマンドを実行する場所)
EXEC_PATH = os.getcwd()

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAmUmQvlG4O72RwibCMQft+t/M1cl/Rnx5cnYrpHQNZCcoAWe7
4+x2jClGcSc3f/5GGE/H6NPxs0zwMEYFRb8BA9I9yYfRnzKluHnw6ICPKmXNXhNr
WlBASWTqYsdWwSEPi6WFGO16naJUs4nBjYGTS4lh1ZytTC/EyDcOEQESNPFHtmse
94fEU7waNKCwVfOM5QHVLNwDFqlz+lgVlcg5PkGVpSwcdQsl9RFRvOnElgdojtNR
2wfalezu2+KIt077jkqG4Zt/d5P6DqBRlBcsPPq7XXf5tYjpWrGdrj/DrHGrBCqo
Rt9r43ARZddpE+jbc96JdkCDQbk2bODhtnvjJwIDAQABAoIBACP+d0OJcuZsTDa3
3S+gOgyH0tR8nStS/T2YbAUQzzguTaGO1zrdArVE1+qoF8sxTQpWaY3NftrofRoI
xyIqiLV5/9I710g3n1xjHeOqlHOTNhcaHkI1x/K0BKmvPzrYZYsYEdnZoco0HQmP
lmiA/bJmDxgW00apjN6qtt3dT4YoqPLaDhalFjwzlYn1D00T4tiaJxlisVAfU6ib
ZaqRP9iKOQuHnbvaVQ4t42KGh6mp3Ev+n1XJ3hEzgZGEWmCwq6w9Wl9KvYgpTvmy
I8JnCnsaApmdZ2TqiKlPT35iMVgTkvxKOTI67KDHYkHr11S5ys93SUHcZMy9av67
uN2chFECgYEAxq7dFDTWH/koFtpOji2J4wjocGmz00HxL9lXzCyEdGJd8tk53T9c
7avYaffmH8L/mNszZH7VLzBoCmDc/cPRwnnGOfg/WRzUGnGk9yDnSV4k7x6cvJsN
SEbYXs+I9B5CwhNmhQpxg1PqC9WJHwLyMQGSg/qSa/Px/RbHSoRdrl8CgYEAxYIj
1/HeXA1cPUjPglLyLHjA4eJAcjEq/Ixp/9FAzRBKBCZ7IlK1PdEqo7l4hSGGClOj
/1HDpfBluMvFP88XJJqHrxDEWyPKDU9o45C8Do1hePFAuvGgv987VJFD+2sIx+e2
jiBuIIbOc3fAIwfP5ZBa8qZJ600keBC8Usk58DkCgYEAvL1GlThwJOV62OK/dz75
WuyOaqNvSYO+C9drGTE9DpaXauhCmNPlgn4Z0ujE+m0yg9HP62q1N+PDIgDMTmEk
NZua3FzgSNYjA4/rxzvBmyfM7D7nZB/jKULrrn12O3k3r8fgPwght0ES9/T9ErGo
wzccKTXyvIx72BI4dahymf8CgYEAlYfGvUnn0AdpaxiByigkIxk05o8VvZ6N7fAc
nEn/ZoFLmELN/JljkC6YuqXDof9UbOMQCVAM8MfFK5hSeNG/sr2vthHapym8YkFZ
pthAGEBfqGH2YNJoontOfuMP9fv+BOLf6lCRL9z/1pm2BI94jVOyF31f/15DGweI
nKCuVbkCgYEAjadONMVV2rpxSOZGi5waDUGSTYdlh//2VgACIvCCxsdyZEClEgI2
MEJwoYo7Z1TPu4C0WXLUtnk+8t8RF9r7WZhKBuPeQwDoP7NGAYsvgDmul/HOHIl3
dYRCg5nZ4iauY2XZPJ4Rsp/fN+uzroUTQlV4TLrmNwaAGiAMQTCKNuQ=
-----END RSA PRIVATE KEY-----"""

RULE = {
    "style_check": {
        "blank_format": {
            "action": True
        },
        "indent": {
            "type": " ", 
            "num": 4,
            "tab_num": 4
        },
        "count_word": {
            "action": True,
            "length": 90
        },
        "line_space": {
            "class_or_global_func": {
                "action": True
            },
            "method": {
                "action": True
            }
        }
    },
    "naming_check": {
        "class_case": {
            "snake": False,
            "CapWords": True
        },
        "method_case": {
            "snake": True,
            "CapWords": False
        },
        "value_case": {
            "snake": True,
            "CapWords": False
        }
    },
    "import_check": {
        "grouping": True,
        "sorting": True
    }
}


def init():
    # カレントパスをtmpに移動
    os.chdir("/tmp")
    # tmpフォルダ内の削除
    os.system('rm -rf /tmp/*')
    # 秘密鍵の作成
    with open("/tmp/id_rsa", "w") as id_rsa:
        id_rsa.write(PRIVATE_KEY)
    os.chmod("/tmp/id_rsa", 0o600)
    # 秘密鍵を環境変数に設定
    os.environ["GIT_SSH_COMMAND"] = 'ssh -i /tmp/id_rsa -o StrictHostKeyChecking=no'
    # Author/Commiterを環境変数に設定
    os.environ["GIT_AUTHOR_NAME"] = "trim-bot"
    os.environ["GIT_AUTHOR_EMAIL"] = "minihitokazu@icloud.com"
    os.environ["GIT_COMMITTER_NAME"] = "trim-bot"
    os.environ["GIT_COMMITTER_EMAIL"] = "minihitokazu@icloud.com"
    

def clone(repo, reponame, branch=None):
    exec_arr = ["git", f"--exec-path={EXEC_PATH}", "clone", repo]
    if branch:
         exec_arr.extend(["-b", branch])
         print(exec_arr)
    subprocess.call(exec_arr)
    # カレントパスを'reponame'に移動
    os.chdir(reponame)
    #print(open("README.md", "r").read())


def local_checkout(new_branch):
    exec_arr = ["git", f"--exec-path={EXEC_PATH}", "checkout", "-b", new_branch]
    subprocess.call(exec_arr)


def local_add_commit(comment):
    exec_add_arr = ["git", f"--exec-path={EXEC_PATH}", "add", "."]
    exec_commit_arr = ["git", f"--exec-path={EXEC_PATH}", "commit", "-m", comment]
    subprocess.call(exec_add_arr)
    subprocess.call(exec_commit_arr)
    

def push(branch="main"):
    exec_arr = ["git", f"--exec-path={EXEC_PATH}", "push", "origin", branch]
    subprocess.call(exec_arr)


# ファイルのパスからファイルを読み込み配列に変換
def read_fp_to_list(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        code_lst = f.readlines()
    return code_lst


# あるファイルパスについて整形処理
def shape_fp(path: str):
    print(f"処理開始: {path}")
    lst_cp = read_fp_to_list(path)
    op = RULE
    
    INDENT_TAB_NUM = op['style_check']['indent']['tab_num']
    
    # コード配列の各要素の行末に改行文字
    lst_cp = add_newline_char(lst_cp)
    
    # compileが通るか確認
    compile_dic = is_comile_to_dic(lst_cp)
    
    if not compile_dic['flag']:
        return
    
    # 空行をきれいにする
    lst_cp = strip_blank_line(lst_cp)
    
    # 末尾空白文字の削除
    lst_cp = delete_blank_ends(lst_cp)
    
    # タブ文字を' '*INDENT_TAB_NUMに置き換え
    lst_cp = replace_tab_to_blank(lst_cp, INDENT_TAB_NUM)
    
    # import部のスプリット
    lst_cp = split_import(lst_cp)
    
    # import部のグルーピング・ソーティング
    #lst_cp = group_sort_import(lst_cp, op['import_check'])
    
    # 走査して、適切なインデントに調節していく 
    lst_cp = scan_indent_config(lst_cp, op['style_check']['indent'])
    
    # 走査して、関数とクラスの整形を行う
    lst_dic = scan_format_method_class(lst_cp, op['style_check']['blank_format'])
    lst_cp = lst_dic['lst']
    def_blank_num = lst_dic['def-blank']
    class_blank_num = lst_dic['class-blank']
    
    # 走査して、関数とクラスの命名規則をチェックする
    lst_dic = scan_naming_method_class(lst_cp, op['naming_check'])
    lst_cp = lst_dic['lst']
    method_naming = lst_dic['method_naming']
    class_naming = lst_dic['class_naming']
    
    # 1行辺りの文字数をチェック
    lst_dic = scan_style_count_word(lst_cp, op['style_check']['count_word'])
    lst_cp = lst_dic['lst']
    s_warn_count = lst_dic['s_warn_count']
    
    # 演算子前後の空白を調整
    lst_cp = scan_operators_space(lst_cp, method_naming, class_naming)
    
    # 改行コードを追加
    lst_cp = add_newline_char(lst_cp)
    
    # 変数の解析と命名規則チェック(コメント削除のため、改行コード優先)
    lst_cp = scan_naming_value(lst_cp, op['naming_check'])
    
    # 整形後の上部に表示するメッセージを作成する
    lst_cp = trim_top_messages(
        lst_cp, 
        op['style_check'], 
        op['import_check'],
        op['naming_check'],
        def_blank_num,
        class_blank_num,
        s_warn_count, # 行辺りの文字数設定
    )
    
    # タブ文字設定の場合は半角X個をタブ文字に変換
    lst_cp = replace_blank_to_tab(lst_cp, op['style_check']['indent']['type'], op['style_check']['indent']['tab_num'])
    
    # 行間の調整
    lst_cp = blank_lines(lst_cp, op['style_check']['line_space'])
    
    # ファイルの上書き
    
    print(lst_cp)
    return


def tree(path, ignore_pathes, layer=0, is_last=False, indent_current='　'):
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())

    # カレントディレクトリの表示
    current = path.split('/')[::-1][0]
    
    if layer == 0:
        print('<'+current+'>')
    else:
        pass
        #branch = '└' if is_last else '├'
        #print('{indent}{branch}<{dirname}>'.format(indent=indent_current, branch=branch, dirname=current))

    # 下の階層のパスを取得
    paths = [p for p in glob.glob(path+'/*') if os.path.isdir(p) or os.path.isfile(p)]
    def is_last_path(i):
        return i == len(paths)-1

    # 再帰的に表示
    for i, p in enumerate(paths):

        indent_lower = indent_current
        if layer != 0:
            indent_lower += '　　' if is_last else '│　'

        if os.path.isfile(p):
            filename = p.split('/')[::-1][0]
            if filename.endswith('.py') and p not in ignore_pathes:
                shape_fp(p)
                break
                #branch = '└' if is_last_path(i) else '├'
                #print('{indent}{branch}{filename}'.format(indent=indent_lower, branch=branch, filename=p.split('/')[::-1][0]))
        if os.path.isdir(p):
            tree(p, ignore_pathes, layer=layer+1, is_last=is_last_path(i), indent_current=indent_lower)


def lambda_handler(event, context):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    
    init()
    clone("git@github.com:tsugitasu-jp/tsugitasu.git", "tsugitasu", "backend")
    local_checkout("prac_from_lambda")
    
    ignore_pathes = [
        "/tmp/tsugitasu/constants.py",
        "/tmp/tsugitasu/config/__init__.py",
        "/tmp/tsugitasu/wsgi.py",
        "/tmp/tsugitasu/__init__.py",
        "/tmp/tsugitasu/users/migrations/0002_photomodel.py",
        "/tmp/tsugitasu/users/migrations/0001_initial.py",
        "/tmp/tsugitasu/users/migrations/__init__.py",
        "/tmp/tsugitasu/users/__init__.py",
        "/tmp/tsugitasu/apiv1/__init__.py",
    ]
    
    # フォルダを走査
    tree(os.getcwd(), ignore_pathes)
    


    
    
    #open(f'README.md', 'a', encoding='utf-8').write(current_time + '\n')
    #local_add_commit("lambdaからpushの練習だよー、バイナリモジュールの用意に苦戦...")
    #push("prac_from_lambda")
    
    





