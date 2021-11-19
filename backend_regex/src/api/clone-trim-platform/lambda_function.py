import subprocess
import os
import datetime
import pathlib
import glob
import json
import urllib.parse
import urllib.request
import logging
import os
import re
import pathlib
import glob
from collections import OrderedDict

import boto3
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, PageBreak, FrameBreak
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import ParagraphStyle
from PIL import Image, ImageOps

from method.is_comile_to_dic import is_comile_to_dic
from method.scan_indent_config import scan_indent_config
from method.naming import scan_naming_method_class, scan_naming_value
from method.import_part.split_import import split_import
from method.import_part.group_sort_impot import group_sort_import
from method.scan_format_method_class import scan_format_method_class
from method.line_checkcount import scan_style_count_word
from method.scan_operators_space import scan_operators_space
from method.blank_lines import blank_lines
from method.create_pdf import create_pdf
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

BUCKET_NAME = 'trim-client'
S3 = boto3.resource('s3')   
S3_CLIENT = boto3.client('s3')

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
         exec_arr.extend(["-b", branch, reponame])
         #print(exec_arr)
    else:
        exec_arr.append(reponame)
    
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


# ファイルのパスからファイルを読み込み、配列に変換
def read_fp_to_list(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        code_lst = f.readlines()
    return code_lst


# 行区切りのリストからファイルに変換し、上書き
def list_to_file(path: str, code_lst: list):
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(code_lst)


# あるファイルパスについて整形処理(戻り値は修正総数)
def shape_fp(path: str, pdf_json: dict, rule: dict) -> int:
    X = 0
    #print(f"処理開始: {path}")
    lst_cp = read_fp_to_list(path)
    
    INDENT_TAB_NUM = rule['style_check']['indent']['tab_num']
    
    # コード配列の各要素の行末に改行文字
    lst_cp = add_newline_char(lst_cp)
    
    # compileが通るか確認
    compile_dic = is_comile_to_dic(lst_cp)
    
    if not compile_dic['flag']:
        pdf_json['code'][-1]['error'] = compile_dic['error']
        X = -1
        return X
     
    # 空行をきれいにする
    lst_cp = strip_blank_line(lst_cp)
    
    # 末尾空白文字の削除
    lst_cp = delete_blank_ends(lst_cp)
    
    # タブ文字を' '*INDENT_TAB_NUMに置き換え
    lst_cp = replace_tab_to_blank(lst_cp, INDENT_TAB_NUM)
    
    # import部のスプリット
    lst_cp = split_import(lst_cp)
    
    # import部のグルーピング・ソーティング
    #lst_cp = group_sort_import(lst_cp, rule['import_check'])
    
    # 走査して、適切なインデントに調節していく 
    lst_cp = scan_indent_config(lst_cp, rule['style_check']['indent'])
    
    # 走査して、関数とクラスの整形を行う
    lst_dic = scan_format_method_class(lst_cp, rule['style_check']['blank_format'])
    lst_cp = lst_dic['lst']
    pdf_json['code'][-1]['blank_method'] = f"{lst_dic['def-blank']}ヵ所"
    X += lst_dic['def-blank']
    pdf_json['code'][-1]['blank_class'] = f"{lst_dic['class-blank']}ヵ所"
    X += lst_dic['class-blank']
    
    # 走査して、関数とクラスの命名規則をチェックする
    lst_dic = scan_naming_method_class(lst_cp, rule['naming_check'])
    lst_cp = lst_dic['lst']
    method_naming = lst_dic['method_naming']
    class_naming = lst_dic['class_naming']
  
    pdf_json['code'][-1]['naming_method'] = f"{len(method_naming.method_hit_lst)}ヵ所"
    X += len(method_naming.method_hit_lst)
    pdf_json['code'][-1]['naming_class'] = f"{len(class_naming.class_hit_lst)}ヵ所"
    X += len(class_naming.class_hit_lst)
    pdf_json['code'][-1]['method_naming_obj'] = method_naming
    pdf_json['code'][-1]['class_naming_obj'] = class_naming
    
    # 1行辺りの文字数をチェック
    lst_dic = scan_style_count_word(lst_cp, rule['style_check']['count_word'])
    lst_cp = lst_dic['lst']
    pdf_json['code'][-1]['len_max_count'] = f"{lst_dic['s_warn_count']}ヵ所"
    X += lst_dic['s_warn_count']
    
    # 演算子前後の空白を調整
    lst_cp, mod_ope_num = scan_operators_space(lst_cp, method_naming, class_naming)
    pdf_json['code'][-1]['blank_value'] = f"{mod_ope_num}ヵ所"
    X += mod_ope_num
    
    # 改行コードを追加
    lst_cp = add_newline_char(lst_cp)
    
    # 変数の解析と命名規則チェック(改行コード優先)
    lst_dic = scan_naming_value(lst_cp, rule['naming_check'])
    lst_cp = lst_dic['lst']
    
    value_naming = lst_dic['value_naming']
    #print(value_naming.value_hit_lst)
    pdf_json['code'][-1]['naming_value'] = f"{len(value_naming.value_hit_lst)}ヵ所"
    X += len(value_naming.value_hit_lst)
    pdf_json['code'][-1]['value_naming_obj'] = value_naming
    
    # タブ文字設定の場合は半角X個をタブ文字に変換
    lst_cp = replace_blank_to_tab(lst_cp, rule['style_check']['indent']['type'], rule['style_check']['indent']['tab_num'])
    
    # 行間の調整
    lst_dic = blank_lines(lst_cp, rule['style_check']['line_space'])
    lst_cp = lst_dic['lst']
    pdf_json['code'][-1]['blank_lines'] = f"{lst_dic['cnt']}ヵ所"
    X += lst_dic['cnt']
    
    # ファイルの上書き
    list_to_file(path, lst_cp)
    
    return X


current = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
pdf_path = "/tmp/trim-result{current}.pdf"

# 日本語が使えるゴシック体のフォントを設定する
font_name = 'HeiseiKakuGo-W5'

WIDTH = portrait(A4)[0]
HEIGHT = portrait(A4)[1]

tree_heihgt = HEIGHT*0.25


def tree(rule, pdf_json, page, path, ignore_pathes, layer=0, is_last=False, indent_current='　'):
    global tree_heihgt
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())
    
    # カレントディレクトリの表示
    current = path.split('/')[::-1][0]
    
    if layer == 0:
        page.drawString(WIDTH*0.10, tree_heihgt, '<'+current+'>')
        tree_heihgt += HEIGHT*0.02
        #print('<'+current+'>')
    else:
        branch = '└' if is_last else '├'
        page.drawString(WIDTH*0.10, tree_heihgt, '{indent}{branch}<{dirname}>'.format(indent=indent_current, branch=branch, dirname=current))
        tree_heihgt += HEIGHT*0.02
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
                suf = r'/tmp/(.*)'  # /tmp/以降が欲しい
                m = re.search(suf, p)
                
                pdf_json["code"].append({
                    "path": m.group(1),
                    "error": None,
                    "blank_method": "-",
                    "blank_class": "-",
                    "blank_value": "-",
                    "len_max_count": "-",
                    "naming_method": "-",
                    "naming_class": "-",
                    "naming_value": "-",
                    "import_sort": "-",
                    "import_group": "-",
                    "line_margin_global": "-",
                    "line_margin_method": "-"
                })
                branch = '└' if is_last_path(i) else '├'
                X = shape_fp(p, pdf_json, rule)
                
                pdf_json['trim_num'] += X
                if X == -1:
                    page.setFillColorRGB(1,0,0)
                    page.drawString(WIDTH*0.10, tree_heihgt, f'{indent_lower}{branch}{filename} ... コンパイルエラー')
                elif X != 0:
                    page.setFillColorRGB(1,0,0)
                    page.drawString(WIDTH*0.10, tree_heihgt, f'{indent_lower}{branch}{filename} ... {X}ヵ所')
                else:
                    page.drawString(WIDTH*0.10, tree_heihgt, f'{indent_lower}{branch}{filename} ... {X}ヵ所')
                page.setFillColorRGB(0,0,0)
                tree_heihgt += HEIGHT*0.02
                pdf_json['file_num'] += 1
                
                #print('{indent}{branch}{filename}'.format(indent=indent_lower, branch=branch, filename=p.split('/')[::-1][0]))
        if os.path.isdir(p):
            tree(rule, pdf_json, page, p, ignore_pathes, layer=layer+1, is_last=is_last_path(i), indent_current=indent_lower)


def post_slack(url_link: str, mes: str):
    send_data = {
        "text": mes,
    }
    send_text = json.dumps(send_data)
    request = urllib.request.Request(
        "https://hooks.slack.com/services/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", 
        data=send_text.encode('utf-8'), 
        method="POST"
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')


def lst_to_str(lst: list, lst_color_target: list):
    s = ''
    for elem in lst:
        if elem in lst_color_target:
            s +=  "<span color=red>" + elem + "&nbsp;&nbsp;&nbsp;&nbsp;</span> "
        else:
            s +=  elem + "&nbsp;&nbsp;&nbsp;&nbsp;"
    return s


def lambda_handler(event, context):
    global tree_heihgt
    tree_heihgt = HEIGHT * 0.25
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("Trim整形=>push処理の開始")
    
    #body_dict = json.loads(event['body'])
    body_dict = event['body']
    
    logger.info(body_dict)
    logger.info(f"pushした人: {body_dict['pusher']['name']}")
    # 整形後のtrim-botからのpushには応答しない
    if body_dict['pusher']['name'] == "trim-bot":
        return
    
    ssh_url = body_dict['repository']['ssh_url']
    repo_id = body_dict['repository']['id']
    repo_name = body_dict['repository']['name']
    logger.info(body_dict['ref'])
    branch = body_dict['ref'].split('/')[-1]
    
    logger.info(f"ssh_url: { ssh_url }")
    logger.info(f"repo_id: { repo_id }")
    logger.info(f"repo_name: { repo_name }")
    logger.info(f"branch: { branch }")
    
    init()
    
    clone(ssh_url, repo_name, branch)
    local_checkout("feature/trim/result")
    
    ignore_pathes = [
        "/tmp/tsugitasu/apiv1/tests.py",
        "/tmp/tsugitasu/apiv1/apps.py",
        "/tmp/tsugitasu/users/admin.py",
        "/tmp/tsugitasu/constants.py",
        "/tmp/tsugitasu/config/settings.py",
        "/tmp/tsugitasu/config/__init__.py",
        "/tmp/tsugitasu/config/urls.py",
        "/tmp/tsugitasu/users/tests.py",
        "/tmp/tsugitasu/users/views.py",
        "/tmp/tsugitasu/wsgi.py",
        "/tmp/tsugitasu/config/tasks.py",
        "/tmp/tsugitasu/apiv1/material_views.py",
        "/tmp/tsugitasu/apiv1/authentication.py",
        "/tmp/tsugitasu/apiv1/decorator.py",
        "/tmp/tsugitasu/manage.py",
        "/tmp/tsugitasu/config/wsgi.py",
        "/tmp/tsugitasu/config/urls.py",
        "/tmp/tsugitasu/config/celeryapp.py",
        "/tmp/tsugitasu/default_override/storage_backends.py",
        "/tmp/tsugitasu/__init__.py",
        "/tmp/tsugitasu/users/migrations/0002_photomodel.py",
        "/tmp/tsugitasu/users/migrations/0001_initial.py",
        "/tmp/tsugitasu/users/migrations/__init__.py",
        "/tmp/tsugitasu/users/__init__.py",
        "/tmp/tsugitasu/apiv1/__init__.py",
    ]

    pdf_json = {
        "file_num": 0,
        "trim_num": 0,
        "code":[]
    }
    
    # rule.jsonの読み込み
    json_open = open('/tmp/tsugitasu/rule.json', 'r')
    rule = json.load(json_open)
    
    # 画像をtmp(img)に保存
    bucket = "trim-techcafeteria"
    img_keys = ["brank_check.png",
                "line_count.png",
                "snake_case.png",
                "CapWords.png",
                "snake_case.png",
                "alpa.png",
                "group.png",
                "global.png",
                "method.png",
                "list_function.png",
                "list_class.png",
                "list_valiablename.png"]
    
    pdf_keys = [
        "indent.png",
        "tab_indent.png",
        "ipaexg.ttf",
        "PDF_plane.pdf",
        "PDF_plane2.pdf",
        "__tmp.pdf"]
    
    os.mkdir('/tmp/img')
    bucket = S3.Bucket(bucket)
    for key in (img_keys + pdf_keys):
        obj_key = "pdf-img/" + key
        file_path = '/tmp/img/' + key
        bucket.download_file(obj_key, file_path)
    
    image_pathes = [
        "/tmp/img/brank_check.png",
        "/tmp/img/brank_check.png",
        "/tmp/img/brank_check.png",
        "/tmp/img/line_count.png",
        "/tmp/img/snake_case.png",
        "/tmp/img/CapWords.png",
        "/tmp/img/snake_case.png",
        "/tmp/img/alpa.png",
        "/tmp/img/group.png",
        "/tmp/img/global.png",
    ]
    
    txt_lst = [
        "空白(関数)",
        "空白(クラス)",
        "空白(その他)",
        "1行の最大文字数",
        "命名-関数",
        "命名-クラス",
        "命名-変数",
        "import ソート",
        "import グループ",
        "ブロック間隔",
    ]
    
    frame_pathes = [
        "/tmp/img/list_function.png",
        "/tmp/img/list_class.png",
        "/tmp/img/list_valiablename.png"
    ]
    
    IMAGE_WIDTH = int((WIDTH - 0.1*WIDTH*2 - 0.05*WIDTH*3)/4)
    IMAGE_FRAME_WIDTH = int(WIDTH-WIDTH*0.20)
    
    def path_to_s3(x):
        image = Image.open(x)
        image = ImageOps.flip(image)
        image = image.resize((IMAGE_WIDTH, int(image.size[1]/(image.size[0]/IMAGE_WIDTH))))
        return image
    
    def path_to_s3_frame(x):
        image = Image.open(x)
        image = ImageOps.flip(image)
        image = image.resize((IMAGE_FRAME_WIDTH, int(image.size[1]/(image.size[0]/IMAGE_FRAME_WIDTH))))
        return image
    
    images = list(map(path_to_s3, image_pathes))
    frames = list(map(path_to_s3_frame, frame_pathes))
    
    # rule.pdfの作成
    create_pdf(rule)
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    
    key = f'{repo_id}/' \
          + f"{current_time}/" \
          + 'trim-rule.pdf' 
          
    S3.Bucket(BUCKET_NAME).upload_file('/tmp/output.pdf', key)
    
    presigned_url = S3_CLIENT.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {'Bucket' : BUCKET_NAME, 'Key' : key},
        ExpiresIn = 3600,
        HttpMethod = 'GET'
    )
    
    mes = f"プロジェクトのルールを可視化しました。\nルールの周知にご活用ください。\nルールpdfは<{presigned_url}|こちら>"
    #post_slack(presigned_url, mes)
    
    
    # A4の新規PDFファイルを作成
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    page = canvas.Canvas(pdf_path, pagesize=portrait(A4), bottomup=False)
    
    # pdfヘッダー
    header_font_size = 14
    page.setFont("HeiseiKakuGo-W5", header_font_size)
    page.drawCentredString(WIDTH/2, HEIGHT*0.075, "整形処理の結果報告")
    
    header2_font_size = 10
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
     
    page.setFont("HeiseiKakuGo-W5", header2_font_size)
    # 発行日時
    page.drawRightString(
        WIDTH*0.975,
        HEIGHT*0.025,
        f"リポジトリID: { repo_id }",
    )
    page.drawRightString(
        WIDTH*0.975,
        HEIGHT*0.04,
        now.strftime('%Y-%m-%d %H:%M'),
    )
    
    # フォルダを走査
    tree(rule, pdf_json, page, os.getcwd(), ignore_pathes)
    
    page.drawString(WIDTH*0.10, HEIGHT*0.125, f"点検ファイル数: {pdf_json['file_num']}件")
    page.drawString(WIDTH*0.10, HEIGHT*0.15, f"総修正箇所: {pdf_json['trim_num']}ヵ所")
    page.drawString(WIDTH*0.10, HEIGHT*0.2, "下記の通り整形いたしました。")
    
    
    bodyStyle = ParagraphStyle('Body', fontName="Helvetica", fontSize=10, leading=16, spaceBefore=0)
    
    dic_map = {
        '0': "blank_method",
        '1': "blank_class",
        '2': "blank_value",
        '3': "len_max_count",
        '4': "naming_method",
        '5': "naming_class",
        '6': "naming_value",
        '7': "import_sort",
        '8': "import_group",
        '9': "blank_lines",
    }
    
    for code_json in pdf_json['code']:
        width_off = WIDTH*0.10 # 画像のoffset
        height_off = HEIGHT*0.05
        txt_off_height = HEIGHT*0.115
        txt_p_off_height = 0
        txt_off_width = 0
        
        # 改ページ
        page.showPage()
        page.setFont("Helvetica", header2_font_size)
        
        page.drawRightString(
            WIDTH*0.975,
            HEIGHT*0.025,
            code_json['path']
        )
        
        page.setFont("HeiseiKakuGo-W5", header2_font_size)
        
        # ファイルがcompile errorの場合
        if code_json['error'] is not None:
            frame = Frame(width_off, height_off, WIDTH-2*width_off, HEIGHT-2*height_off, showBoundary=1)
            bodyStyle = ParagraphStyle('Body', fontName="Helvetica", fontSize=10, leading=28, spaceBefore=0)
            message = code_json['error'].replace('\n', '<br />')
            
            para1 = Paragraph(message, style=bodyStyle)
            w, h = para1.wrap(WIDTH, HEIGHT)
            para1.drawOn(page, width_off, height_off-h+30) # 30はオフセット
            #frame.addFromList([para1], page) 
            
            continue
        
        page.drawCentredString(
            WIDTH*0.5,
            HEIGHT*0.065,
            "ルール適応一覧"
        )
        
        for i, image in enumerate(images):
            page.drawInlineImage(image, width_off, height_off)
            
            if i == 0:
                txt_p_off_height = HEIGHT*0.115+image.size[1]+15
            if i % 4 == 0:
                txt_off_width = WIDTH*0.10+image.size[0]/2
            else:
                txt_off_width += (WIDTH*0.05+image.size[0])
            
            txt = txt_lst[i]
            
            display_point_txt = code_json[dic_map[str(i)]]
            
            page.setFillColorRGB(0,0,0)
            page.drawCentredString(txt_off_width, txt_off_height, txt)
            
            
            if code_json[dic_map[str(i)]] == "0ヵ所" or code_json[dic_map[str(i)]] == '-':
                page.setFillColorRGB(0,0,0)
            elif (dic_map[str(i)] == "blank_method" \
                or dic_map[str(i)] == "blank_class" \
                or dic_map[str(i)] == "blank_value" \
                or dic_map[str(i)] == "blank_lines"):
                #print(code_json[dic_map[str(i)]])
                page.setFillColorRGB(34/255,139/255,34/255)
            elif (dic_map[str(i)] == "naming_method" \
                or dic_map[str(i)] == "naming_class" \
                or dic_map[str(i)] == "naming_value" \
                or dic_map[str(i)] == "len_max_count"):
                page.setFillColorRGB(255/255,140/255,0)
            else:
                page.setFillColorRGB(0,0,0)
            
            page.drawCentredString(txt_off_width, txt_p_off_height, display_point_txt)
            
            
            width_off += (image.size[0] + WIDTH*0.05)
            if (i+1) % 4 == 0:
                height_off += HEIGHT*0.125
                width_off = WIDTH*0.10
                txt_off_height += HEIGHT*0.125
                txt_p_off_height += HEIGHT*0.125
        
        txt_off_height = HEIGHT*0.525
        
        page.setFillColorRGB(0,0,0)
        page.drawCentredString(
            WIDTH*0.5,
            txt_off_height,
            "命名リスト"
        )
        
        # image frameの描画
        img_off_height = HEIGHT*0.46
        
        s_method_naming = lst_to_str(code_json['method_naming_obj'].method_lst, code_json['method_naming_obj'].method_hit_lst)
        s_class_naming = lst_to_str(code_json['class_naming_obj'].class_lst, code_json['class_naming_obj'].class_hit_lst)
        s_value_naming = lst_to_str(code_json['value_naming_obj'].value_lst, code_json['value_naming_obj'].value_hit_lst)
        s_lst = [s_method_naming , s_class_naming, s_value_naming]
        
        
        for i, frame_image in enumerate(frames):
            page.drawInlineImage(frame_image, WIDTH*0.10, img_off_height)
            img_off_height += (image.height + 15*mm)
            frame = Frame(WIDTH*0.10, img_off_height, 0.79*WIDTH, image.height-30, showBoundary=1)
            para = Paragraph(s_lst[i], style=bodyStyle)
            w, h = para.wrap(0.79*WIDTH, image.height-30)
            para.drawOn(page, 0.11*WIDTH, img_off_height-h+35) # 35はオフセット
            
    page.save()

    
    local_add_commit("@trim 整形結果の反映")
    push("feature/trim/result")
    
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    
    
    key = f'{repo_id}/' \
          + f"{current_time}/" \
          + 'trim-result.pdf'
          
    S3.Bucket(BUCKET_NAME).upload_file(pdf_path, key)
    
    presigned_url = S3_CLIENT.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {'Bucket' : BUCKET_NAME, 'Key' : key},
        ExpiresIn = 3600,
        HttpMethod = 'GET'
    )
    
    mes = f"リポジトリに対し、整形処理を行いました。\n整形結果レポートは<{presigned_url}|こちら>"
    #post_slack(presigned_url, mes)
    
    
    return presigned_url