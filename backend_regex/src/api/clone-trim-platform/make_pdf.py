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
header_font_size = 14
page.setFont("HeiseiKakuGo-W5", header_font_size)
page.drawCentredString(WIDTH/2, HEIGHT*0.075, "整形処理の結果報告")

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


page.drawCentredString(
    WIDTH*0.5,
    HEIGHT*0.065,
    "ルール適応一覧"
)

image_pathes = [
    "img/brank_check.png",
    "img/brank_check.png",
    "img/brank_check.png",
    "img/line_count.png",
    "img/snake_case.png",
    "img/CapWords.png",
    "img/snake_case.png",
    "img/alpa.png",
    "img/group.png",
    "img/global.png",
    "img/method.png"
]

frame_pathes = [
    "img/list_function.png",
    "img/list_class.png",
    "img/list_valiablename.png"
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
        height_off += HEIGHT*0.125
        width_off = WIDTH*0.10
        txt_off_height += HEIGHT*0.125
        txt_p_off_height += HEIGHT*0.125

txt_off_height = HEIGHT*0.525

page.drawCentredString(
    WIDTH*0.5,
    txt_off_height,
    "命名リスト"
)

img_off_height = HEIGHT*0.46

IMAGE_FRAME_WIDTH = int(WIDTH-WIDTH*0.20)


from reportlab.platypus import Paragraph, PageBreak, FrameBreak
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import ParagraphStyle

bodyStyle = ParagraphStyle('Body', fontName="HeiseiKakuGo-W5", fontSize=10, leading=16, spaceBefore=0)

for path in frame_pathes:
    image =Image.open(path)
    image = ImageOps.flip(image)
    image = image.resize((IMAGE_FRAME_WIDTH, int(image.size[1]/(image.size[0]/IMAGE_FRAME_WIDTH))))
    page.drawInlineImage(image, WIDTH*0.10, img_off_height)
    
    img_off_height += (image.height + 10*mm)
    frame = Frame(WIDTH*0.10, img_off_height, 0.8*WIDTH, image.height-30, showBoundary=1)
    para = Paragraph("  aaaaaa  aaaaaaaa  aaaaaaaaa aaaaaaaaa  aaaaaaaaa aaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", style=bodyStyle)
    w, h = para.wrap(0.8*WIDTH, image.height-30)
    para.drawOn(page, 0.11*WIDTH, img_off_height-h+22) # 22はオフセット
    




#img_txt_height = HEIGHT * 0.62
#frame = Frame(WIDTH*0.10, img_off_height, 0.8*WIDTH, image.height-30, showBoundary=1)
#bodyStyle = ParagraphStyle('Body', fontName="HeiseiKakuGo-W5", fontSize=10, leading=16, spaceBefore=0)

#para1 = Paragraph("  aaaaaa  aaaaaaaa  aaaaaaaaa aaaaaaaaa  aaaaaaaaa aaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", style=bodyStyle)
#w, h = para1.wrap(0.8*WIDTH, image.height-30)
#print((w, h))
#para1.drawOn(page, 0.11*WIDTH, img_off_height-h+22) # 22はオフセット
#frame.addFromList([para1], page) 


#txt_off_width = WIDTH*0.10
#for i, method in enumerate(method_lst):
#    page.drawString(txt_off_width, txt_off_height, method)
#    txt_off_width += (WIDTH*0.05 + image.size[0])
#    if (i+1) % 2 == 0:
#        txt_off_width = WIDTH*0.10
#        txt_off_height += HEIGHT*0.0125


# PDFファイルとして保存
page.save()
