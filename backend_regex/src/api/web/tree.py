import pathlib
import glob
import os
import re

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors

file_path = "tree.pdf"

# 日本語が使えるゴシック体のフォントを設定する
font_name = 'HeiseiKakuGo-W5'
pdfmetrics.registerFont(UnicodeCIDFont(font_name))

# A4の新規PDFファイルを作成
page = canvas.Canvas(file_path, pagesize=portrait(A4), bottomup=False)
WIDTH = portrait(A4)[0]
HEIGHT = portrait(A4)[1]

font_size = 14
page.setFont("HeiseiKakuGo-W5", font_size)

#page.drawString(WIDTH*0.10, HEIGHT*0.225, "下記の通り整形いたしました。")
tree_heihgt = portrait(A4)[1]*0.2

def tree(path, layer=0, is_last=False, indent_current='　'):
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
            tree(p, layer=layer+1, is_last=is_last_path(i), indent_current=indent_lower)

tree('./')
page.save()