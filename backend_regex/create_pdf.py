
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ルールに関するPDFを output.pdf として出力 (PDF_plane.pdfをベース)
def create_pdf(rule: dict):
    snake_path = "input\img\snake_case.png"
    capword_path = "input\img\CapWords形式.png"
    rule_array =[["予約語や変数間の空白","input\img\空白・スペースのチェック.png","classや関数、演算子前後を空白で整形する機能です。"],
    ["インデントのスペース数", "input\img\\tabインデント.png", "インデントであけるスペースの数を設定できます。"],
    ["一行あたりの文字数","input\img\一行文字.png"," 一行あたりの文字数を決めます。"],
    ["クラス・グローバル関数間の間隔","input\img\メソッドブロック間の間隔.png","クラス・グローバル関数ブロックの上下を2行空けるかを決めます。"],
    ["メソッドブロック間の間隔","input\img\クラス・グローバル関数の間隔.png", "メソッドブロックの上下を1行空けるかを決めます。"],
    ["クラスの命名規則","input\img\CapWords形式.png","クラスの命名規則を決めます。チェック：CapWords, 未チェック：Snake"],
    ["関数の命名規則","input\img\CapWords形式.png","関数の命名規則を決めます。チェック：CapWords, 未チェック：Snake"],
    ["変数の命名規則", "input\img\snake_case.png","変数の命名規則を決めます。チェック：CapWords, 未チェック：Snake"],
    ["グルーピング", "input\img\グルーピング.png","インポートを種類によって、振り分けを行う機能です。"],
    ["アルファベット順並び替え", "input\img\アルファベット順.png", "アルファベット順に並び替える機能です。"],
    ]


    #適用済みのルールのみ適用 + 変数をrule.jsonから読み込み表示
    adapted_rule = []
    if rule["style_check"]["blank_format"]['action']:
        rule_array[0].append("チェック :  ON")
        adapted_rule.append(rule_array[0])
    if rule["style_check"]["indent"]["type"] == " ":
        rule_array[1].append(f"スペース数 : {rule['style_check']['indent']['num']}")
    elif rule["style_check"]["indent"]["type"] == "\t":
        rule_array[1].append(f"タブ数 : {rule['style_check']['indent']['tab_num']}")
    adapted_rule.append(rule_array[1]) #indent
    rule_array[2].append(f"1行あたりの文字 : {rule['style_check']['count_word']['length']}文字 ")
    adapted_rule.append(rule_array[2]) #count_word
    if rule["style_check"]['line_space']['class_or_global_func']['action']:
        rule_array[3].append("チェック :  ON")
        adapted_rule.append(rule_array[3]) #'class_or_global_func'
    if rule["style_check"]['line_space']['method']['action']:
        rule_array[4].append("チェック :  ON")
        adapted_rule.append(rule_array[4]) #method
    if rule['naming_check']['class_case']['snake']:
        rule_array[5].append("未チェック : snake_case")
        rule_array[5][1] = snake_path
    else:
        rule_array[5].append("チェック済 : CapWords")
        rule_array[5][1] = capword_path
    adapted_rule.append(rule_array[5]) #class and method _case

    if rule['naming_check']['class_case']['snake']:
        rule_array[6].append("未チェック : snake_case")
        rule_array[6][1] = snake_path
    else:
        rule_array[6].append("チェック済 : CapWords")
        rule_array[6][1] = capword_path
    adapted_rule.append(rule_array[6]) #class and method _case

    if rule['naming_check']['value_case']['snake']:
        rule_array[7].append("未チェック : snake_case")
        rule_array[7][1] = snake_path
    else:
        rule_array[7].append("チェック済 : CapWords")
        rule_array[7][1] = capword_path
    adapted_rule.append(rule_array[7]) #variable_case

    if rule['import_check']['grouping']:
        rule_array[8].append("チェック :  ON")
        adapted_rule.append(rule_array[8]) #grouping

    if rule['import_check']['sorting']:
        rule_array[9].append("チェック :  ON")
        adapted_rule.append(rule_array[9]) #sorting
    adapted_rule


    # ファイルの指定
    template_file = './PDF_plane.pdf' # 既存のテンプレートPDF
    output_file = './output.pdf' # 完成したPDFの保存先
    tmp_file = './__tmp.pdf' # 一時ファイル

    # A4縦のCanvasを作成 -- (*1)
    w, h = portrait(A4)
    cv = canvas.Canvas(tmp_file, pagesize=(w, h))
    cv2 = canvas.Canvas(tmp_file, pagesize=(w, h))

    # フォントを登録しCanvasに設定 --- (*2)
    ttf_file = './ipaexg.ttf'
    pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))

    head_pos = 42
    rule_num = 0
    cv.setFillColorRGB(0, 0, 0)
    str_interval = 43

    for i in range(len(adapted_rule)):
        if i<=5:
            # 文字列を描画する --- (*3)
            # タイトル設定
            cv.setFont('IPAexGothic', 14)
            cv.drawString(80*mm, h-(head_pos+str_interval*(rule_num % 6))*mm, adapted_rule[rule_num][0])
            cv.setFont('IPAexGothic', 10)
            cv.drawString(80*mm, h-((head_pos+10)+str_interval*(rule_num % 6))*mm, adapted_rule[rule_num][2])
            cv.setFont('IPAexGothic', 15)
            cv.drawString(80*mm, h-((head_pos+25)+str_interval*(rule_num % 6))*mm, adapted_rule[rule_num][3])
            #画像を挿入
            cv.drawImage(adapted_rule[rule_num][1], 15*mm, h-(70+43*(rule_num % 6))*mm)
            rule_num += 1
        elif i<=11:
            # 文字列を描画する --- (*3)
            # タイトル設定
            cv2.setFont('IPAexGothic', 14)
            cv2.drawString(80*mm, h-(head_pos+str_interval*(rule_num % 6))*mm, adapted_rule[rule_num][0])
            cv2.setFont('IPAexGothic', 10)
            cv2.drawString(80*mm, h-((head_pos+10)+str_interval*(rule_num % 6))*mm, adapted_rule[rule_num][2])
            cv2.setFont('IPAexGothic', 15)
            cv2.drawString(80*mm, h-((head_pos+25)+str_interval*(rule_num % 6))*mm, adapted_rule[rule_num][3])
            #画像を挿入
            cv2.drawImage(adapted_rule[rule_num][1], 15*mm, h-(70+43*(rule_num % 6))*mm)
            rule_num += 1

    if len(adapted_rule)<=6:
        # 一時ファイルに保存 --- (*4)
        cv.showPage()
        cv.save()

        # テンプレートとなるPDFを読む --- (*5)
        template_pdf = PdfFileReader(template_file)
        template_page = template_pdf.getPage(0)

        # 一時ファイルを読んで合成する --- (*6)
        tmp_pdf = PdfFileReader(tmp_file)
        template_page.mergePage(tmp_pdf.getPage(0))
        # 書き込み先PDFを用意 --- (*7)
        output = PdfFileWriter()
        output.addPage(template_page)


    elif len(adapted_rule)<=12:
        # 一時ファイルに保存 --- (*4)
        cv.showPage()
        cv.save()

        # テンプレートとなるPDFを読む --- (*5)
        template_pdf = PdfFileReader('./PDF_plane2.pdf')
        template_page = template_pdf.getPage(0)

        # 一時ファイルを読んで合成する --- (*6)
        tmp_pdf = PdfFileReader(tmp_file)
        template_page.mergePage(tmp_pdf.getPage(0))
        # 書き込み先PDFを用意 --- (*7)
        output = PdfFileWriter()
        output.addPage(template_page)

        # 一時ファイルに保存 --- (*4)
        cv2.showPage()
        cv2.save()
        # テンプレートとなるPDFを読む --- (*5)
        template_page = template_pdf.getPage(1)
        # 一時ファイルを読んで合成する --- (*6)
        tmp_pdf = PdfFileReader(tmp_file)
        template_page.mergePage(tmp_pdf.getPage(0))
        output.addPage(template_page)

    with open(output_file, "wb") as fp:
       output.write(fp)