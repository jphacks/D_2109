import os
import re
import pathlib
import glob

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors

from PIL import Image, ImageOps


pdf_path = "sample.pdf"

# 日本語が使えるゴシック体のフォントを設定する
font_name = 'HeiseiKakuGo-W5'
pdfmetrics.registerFont(UnicodeCIDFont(font_name))

# A4の新規PDFファイルを作成
page = canvas.Canvas(pdf_path, pagesize=portrait(A4), bottomup=False)
WIDTH = portrait(A4)[0]
HEIGHT = portrait(A4)[1]


tree_heihgt = HEIGHT*0.25

def tree(path, ignore_pathes, layer=0, is_last=False, indent_current='　'):
    global tree_heihgt
    if not pathlib.Path(path).is_absolute():
        path = str(pathlib.Path(path).resolve())

    path = re.sub('\\\\', '/', path)
    
    # カレントディレクトリの表示
    current = re.split('/', path)[::-1][0]
    
    if layer == 0:
        page.drawString(WIDTH*0.10, tree_heihgt, '<'+current+'>')
        tree_heihgt += HEIGHT*0.02
        print('<'+current+'>')
    else:
        branch = '└' if is_last else '├'
        page.drawString(WIDTH*0.10, tree_heihgt, '{indent}{branch}<{dirname}>'.format(indent=indent_current, branch=branch, dirname=current))
        tree_heihgt += HEIGHT*0.02
        print('{indent}{branch}<{dirname}>'.format(indent=indent_current, branch=branch, dirname=current))

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
            if filename.endswith('.py'):
                branch = '└' if is_last_path(i) else '├'
                page.drawString(WIDTH*0.10, tree_heihgt, '{indent}{branch}{filename} ... Xヵ所'.format(indent=indent_lower, branch=branch, filename=filename))
                tree_heihgt += HEIGHT*0.02
                print('{indent}{branch}{filename} ... Xヵ所'.format(indent=indent_lower, branch=branch, filename=filename))
        if os.path.isdir(p):
            tree(p, ignore_pathes, layer=layer+1, is_last=is_last_path(i), indent_current=indent_lower)

# ヘッダー
header_font_size = 24
page.setFont("HeiseiKakuGo-W5", header_font_size)
page.drawCentredString(WIDTH/2, HEIGHT*0.075, "[Trim] 整形処理の報告書")

header2_font_size = 10
page.setFont("HeiseiKakuGo-W5", header2_font_size)
# 発行日時
page.drawRightString(
    WIDTH*0.975,
    HEIGHT*0.025,
    "リポジトリID: xxxxx",
)
page.drawRightString(
    WIDTH*0.975,
    HEIGHT*0.04,
    "xxxx-xx-xx xx:xx",
)

page.drawString(WIDTH*0.10, HEIGHT*0.125, "点検ファイル数: xxxx件")
page.drawString(WIDTH*0.10, HEIGHT*0.15, "総修正箇所: xxxヵ所")
page.drawString(WIDTH*0.10, HEIGHT*0.2, "下記の通り整形いたしました。")

ignore_pathes = []
tree('./', ignore_pathes)

############ 改ページ
page.showPage()
page.setFont("HeiseiKakuGo-W5", header2_font_size)

page.drawRightString(
    WIDTH*0.975,
    HEIGHT*0.025,
    "xxx/yyyaaaaaaaaaaaaaaaaaaaaaaa/zzz.py"
)

image_pathes = [
    "img/空白・スペースのチェック.png",
    "img/空白・スペースのチェック.png",
    "img/空白・スペースのチェック.png",
    "img/1行文字.png",
    "img/snake_case.png",
    "img/CapWords形式.png",
    "img/snake_case.png",
    "img/アルファベット順.png",
    "img/グルーピング.png",
    "img/グローバル間隔.png",
    "img/メソッドブロック間の間隔.png"
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
    "間隔 グローバル",
    "間隔 クラスメソッド"
]

method_lst = [
    "add_box",
    "add_box",
    "add_box",
    "add_box",
    "add_box",
    "add_box",
    "add_box",
    "add_box",
    "add_box",
    "add_box",
    "add_box",
]

IMAGE_WIDTH = int((WIDTH - 0.1*WIDTH*2 - 0.05*WIDTH*3)/4)
width_off = WIDTH*0.10 # 画像のoffset
height_off = HEIGHT*0.05
txt_off_height = HEIGHT*0.115
txt_p_off_height = 0
txt_off_width = 0

for i, path in enumerate(image_pathes):
    image =Image.open(path)
    image = ImageOps.flip(image)
    image = image.resize((IMAGE_WIDTH, int(image.size[1]/(image.size[0]/IMAGE_WIDTH))))
    page.drawInlineImage(image, width_off, height_off)
    
    if i == 0:
        txt_p_off_height = HEIGHT*0.115+image.size[1]+15
    if i % 4 == 0:
        txt_off_width = WIDTH*0.10+image.size[0]/2
    else:
        txt_off_width += (WIDTH*0.05+image.size[0])
    
    txt = txt_lst[i]
    page.drawCentredString(txt_off_width, txt_off_height, txt)
    page.drawCentredString(txt_off_width, txt_p_off_height, "xヵ所")
    
    width_off += (image.size[0] + WIDTH*0.05)
    if (i+1) % 4 == 0:
        height_off += HEIGHT*0.15
        width_off = WIDTH*0.10
        txt_off_height += HEIGHT*0.15
        txt_p_off_height += HEIGHT*0.15

txt_off_height += HEIGHT*0.025 + HEIGHT*0.15
rect_method = page.rect(WIDTH*0.10, txt_off_height, WIDTH*0.80, HEIGHT*0.10)
rect_class = page.rect(WIDTH*0.10, txt_off_height+HEIGHT*0.115, WIDTH*0.80, HEIGHT*0.10)
rect_value = page.rect(WIDTH*0.10, txt_off_height+HEIGHT*0.23, WIDTH*0.80, HEIGHT*0.10)


txt_off_width = WIDTH*0.10
for i, method in enumerate(method_lst):
    page.drawString(txt_off_width, txt_off_height, method)
    txt_off_width += (WIDTH*0.05 + image.size[0])
    if (i+1) % 2 == 0:
        txt_off_width = WIDTH*0.10
        txt_off_height += HEIGHT*0.0125


# PDFファイルとして保存
page.save()
