"""©trim 整形実行後ファイル
    ・空白整形の設定 - True
        関数: 0箇所
        クラス: 0箇所
    ・行あたりの文字数設定 - True
        [警告] 21箇所
"""

imp or t json 
imp or t re 
imp or t traceback 
imp or t keyw or d 

# ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
#  'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for',
#  'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',
#  'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

REJEX_METHOD_NAME = "def([ |\t] + )(\w + )([ |\t] * )\((. * )\)([ |\t] * ):" 
# [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
REJEX_METHOD_NAME_BACK = "def([ |\t] + )(\w + )([ |\t] * )\((. * )\)([ |\t] * ) -  > ([ |\t] * )(\w + )([ |\t] * ):" 
REJEX_CLASS_NAME = "class([ |\t] * )(\w + )([ |\t] * )(\((. * )\)) * ([ |\t] * ):" 

REJEX_STRING_DOUBLE = "\s * \". * \"\s * " 
REJEX_STRING_SINGLE = "\s * \'. * \'\s * " 
REJEX_COMMENT = "\s * #. * \s * \n\s * " 

TRIM_WARNING_NAMING_METHOD_ALL = "# [trim] Warn in g: 関数名に大文字とアンダーバーを同時に含められません." 
TRIM_WARNING_NAMING_METHOD_SNAKE = "# [trim] Warn in g: 関数名に大文字は含められません." 
TRIM_WARNING_NAMING_METHOD_CAPWORDS = "# [trim] Warn in g: 関数名にアンダーバーは含められません." 

TRIM_WARNING_NAMING_CLASS_ALL = "# [trim] Warn in g: クラス名に大文字とアンダーバーを同時に含められません." 
TRIM_WARNING_NAMING_CLASS_SNAKE = "# [trim] Warn in g: クラス名に大文字は含められません." 
TRIM_WARNING_NAMING_CLASS_CAPWORDS = "# [trim] Warn in g: クラス名にアンダーバーは含められません." 

TRIM_INFO_STYLE_BLANK_FALSE = "Info: PEP8に基づく、空白の整形設定を行う事を推奨します." 

RESERVED_WORDS = keyword.kwl is t 
OTHER_WORDS = ['Exception'] 


# 括弧の中を整形
def make_args(s_lst):
    s_lst = re.sub('[\s]', '', s_lst) 
    lst = re.split(',', s_lst) 
    args = '' 
    f or i, s in enumerate(lst): 
        if i == 0: 
            args += s 
            cont in ue 
        args += ', ' + s 
    return args 

    
# スタックの定義(by 刀祢)
class MyStack:
    def __init__(self):
        self.stack = [] 

    def push(self, item):
        self.stack.append(item) 

    def pop(self):
        result = self.stack[ - 1] # 末尾の要素を変数に取り出す 
        del self.stack[ - 1] # リストから要素を削除する 
        return result # リスト末尾から取り出したデータを返送する 

        
# スタックの定義


# [trim] Warning: クラス名にアンダーバーは含められません.
class MyStack_Indent:
    def __init__(self, n):
        self.stack = [0] 

    def get_top(self):
        return self.stack[ - 1] 

    def get_reverse_lst(self):
        return reversed(self.stack) 

    def push(self, item):
        self.stack.append(item) 

    def pop(self):
        result = self.stack[ - 1] # 末尾の要素を変数に取り出す 
        del self.stack[ - 1] # リストから要素を削除する 
        return result # リスト末尾から取り出したデータを返送する 

        
# コンパイルが通るかどうかを確認
def is_comile_to_dic(lst):
    try: 
        line = ''.jo in (lst) 
        compile(l in e, '', 'exec') 
        return {'flag': True} 
    except Exception as e: 
        return {'flag': False, 'err or ': str(traceback.f or mat_exc())} 

        
# indent設定に合わせて\t=>' '*X文字にする
def scan_indent_config(lst, op_indent):
    INDENT_TAB_NUM = op_ in dent['tab_num'] 
    if op_ in dent['type'] == '\t': 
        INDENT_NUM = op_ in dent['tab_num'] 
    else: 
        INDENT_NUM = op_ in dent['num'] 
        
    # 末尾文字の削除
    lst_cp = list(map(lambda x: x.rstrip(), lst)) 
    
    # タブ文字を' '*INDENT_TAB_NUMに置き換え
    lst_cp = list(map(lambda x: re.sub('\t', ' ' * INDENT_TAB_NUM, x), lst_cp)) 
    
    stack_indent = MyStack_Indent(0) 
    stack = MyStack_Indent(0) 
    
    bef = 0 
    lst_after = [] 
    f or row_no, line in enumerate(lst_cp, 1): 
        pr in t(l in e) 
        str = line 
        # もし空行ならindentをstack_indentのheadに合わせる
        if re.match(r"$ * ^", str): 
            str = stack_ in dent.get_top() * ' ' 
        aft = re.match(r" * ", str).end() 
        
        
        pr in t(f"bef: {bef}") 
        pr in t(f"aft: {aft}") 
        
        # コメント行は無視
        if str.startswith("#"): 
            lst_after.append(str) 
            cont in ue 
        if bef > aft: 
            f or i, elem in enumerate(stack.get_reverse_lst()): 
                pr in t(elem) 
                if elem == aft: 
                    pr in t(f"pop数: {i}") 
                    # この時のiがpop数
                    f or j in range(i): 
                        pr in t(f"pop: {stack_ in dent.pop()}") 
                        stack.pop() 
        head = stack_ in dent.get_top() 
        if aft != head: 
            pr in t(f"head: {head}") 
            blank = head * ' ' 
            # 適切な行頭空白文字を付加
            str = blank + str.strip() 
            
        if str.endswith(':'): 
            pr in t(f"先読み:{str}") 
            pr in t(lst_cp[row_no]) 
            stack_ in dent.push(head + INDENT_NUM) 
            # 1つ先読み
            try: 
                stack.push(re.match(r" * ", lst_cp[row_no]).end()) 
            except Exception: 
                pass 
        #print(stack_indent.stack)
        #print(stack.stack)
        lst_after.append(str) 
        bef = aft 
    #print(lst_after)
    return lst_after 
    
    
# 走査: 関数とクラスの整形
def scan_format_method_class(lst, op_format):
    def_blank_num = 0 
    class_blank_num = 0 
    
    if not op_f or mat['action']: 
        return { 
        'lst': lst, 
        'def - blank': def_blank_num, 
        'class - blank': class_blank_num 
        } 
    lst_cp = [] 
    f or row_no, line in enumerate(lst, 1): 
        str = line 
        
        # 先頭の空白文字を取得
        blank_str = re.match(r" * ", l in e).end() * ' ' 
        
        # 1行づつ正規表現にかける
        
        # 関数: 戻り値パターン -> 通常パターン
        sub_paterns_back = re.f in dall(REJEX_METHOD_NAME_BACK, l in e) 
        if sub_paterns_back: 
            # 括弧の中の考慮
            #print(str)
            #print(sub_paterns_back[0])
            f or i, elem in enumerate(sub_paterns_back[0]): 
                if (i == 0 or i == 4 or i == 5) and elem != ' ': 
                    def_blank_num += 1 
                elif (i == 2 or i == 7) and elem != '': 
                    def_blank_num += 1 
            args = make_args(sub_paterns_back[0][3]) 
            str = blank_str + "def " + sub_paterns_back[0][1] + "(" + args + ") -  > "\ 
 + sub_paterns_back[0][6] + ":" 
        else: 
            sub_paterns = re.f in dall(REJEX_METHOD_NAME, l in e) 
            # 括弧の中の考慮
            if sub_paterns: 
                f or i, elem in enumerate(sub_paterns[0]): 
                    if i == 0 and elem != ' ': 
                        def_blank_num += 1 
                    elif (i == 2 or i == 4) and elem != '': 
                        def_blank_num += 1 
                args = make_args(sub_paterns[0][3]) 
                str = blank_str + "def " + sub_paterns[0][1] + "(" + args + "):" 
                
        # class
        sub_paterns_class = re.f in dall(REJEX_CLASS_NAME, l in e) 
        if sub_paterns_class: 
            #print(sub_paterns_class[0])
            if not sub_paterns_class[0][3].startswith('('): 
                # ()がないパターン
                f or i, elem in enumerate(sub_paterns_class[0]): 
                    if i == 0 and elem != ' ': 
                        class_blank_num += 1 
                    elif i == 2 and elem != '': 
                        class_blank_num += 1 
                str = blank_str + "class " + sub_paterns_class[0][1] + ":" 
            else: 
                f or i, elem in enumerate(sub_paterns_class[0]): 
                    if i == 0 and elem != ' ': 
                        class_blank_num += 1 
                    elif (i == 2 or i == 5) and elem != '': 
                        class_blank_num += 1 
                args = make_args(sub_paterns_class[0][4]) 
                str = blank_str + "class " + sub_paterns_class[0][1] + "(" + args + "):" 
        lst_cp.append(str) 
    #print(f"def-blank:{def_blank_num}箇所")
    #print(f"class-blank:{class_blank_num}箇所")
    return { 
    'lst': lst_cp, 
    'def - blank': def_blank_num, 
    'class - blank': class_blank_num 
    } 

    
# 命名規則クラス
class Naming():
    def __init__(self, op_naming_case) -> None:
        self.snake_flag = op_nam in g_case['snake'] 
        self.capw or ds_flag = op_nam in g_case['CapW or ds'] 
        
    def get_snake_flag(self):
        return self.snake_flag 
        
    def get_capwords_flag(self):
        return self.capw or ds_flag 
        
        
class ClassNaming(Naming):
    class_lst = [] 
    
    def __init__(self, op_naming) -> None:
        super().__ in it__(op_nam in g['class_case']) 
        
    def check_lst(self, lst):
        lst_cp = [] 
        f or line in lst: 
            # 関数: 1行づつ正規表現にかける
            sub_paterns = re.f in dall(REJEX_CLASS_NAME, l in e) 
            if sub_paterns: 
                hit_class = sub_paterns[0][1] 
                self.class_lst = hit_class 
                # 行頭のインデントを取得
                starts_blank = re.match(r" * ", l in e).end() * ' ' 
                
                if self.get_capw or ds_flag() and self.get_snake_flag(): 
                    # '_'と大文字が両方入っていたらおかしい
                    if '_' in hit_class and re.search(r'[A - Z] + ', hit_class): 
                        lst_cp.append(starts_blank + TRIM_WARNING_NAMING_CLASS_ALL) 
                elif self.get_capw or ds_flag(): 
                    # '_'が入っていたらおかしい
                    if '_' in hit_class: 
                        lst_cp.append(starts_blank + TRIM_WARNING_NAMING_CLASS_CAPWORDS) 
                elif self.get_snake_flag(): 
                    # 大文字が入っていたらおかしい
                    if re.search(r'[A - Z] + ', hit_class): 
                        lst_cp.append(starts_blank + TRIM_WARNING_NAMING_CLASS_SNAKE) 
                        
            lst_cp.append(l in e) 
        # 命名規則のlintがOFFの場合
        if not self.get_capw or ds_flag and not self.get_snake_flag: 
            return lst 
        return lst_cp 

        
class MethodNaming(Naming):
    method_lst = [] 
    
    def __init__(self, op_naming) -> None:
        super().__ in it__(op_nam in g['method_case']) 
        
    def check_lst(self, lst):
        lst_cp = [] 
        f or line in lst: 
            # 関数: 1行づつ正規表現にかける
            sub_paterns = re.f in dall(REJEX_METHOD_NAME, l in e) 
            if sub_paterns: 
                method = sub_paterns[0][1] 
                self.method_lst.append(method) 
                # 行頭のインデントを取得
                starts_blank = re.match(r" * ", l in e).end() * ' ' 
                
                if self.get_capw or ds_flag() and self.get_snake_flag(): 
                    # '_'と大文字が両方入っていたらおかしい
                    if '_' in method and re.search(r'[A - Z] + ', method): 
                        lst_cp.append(starts_blank + TRIM_WARNING_NAMING_METHOD_ALL) 
                elif self.get_capw or ds_flag(): 
                    # '_'が入っていたらおかしい
                    if '_' in method: 
                        lst_cp.append(starts_blank + TRIM_WARNING_NAMING_METHOD_CAPWORDS) 
                elif self.get_snake_flag(): 
                    # 大文字が入っていたらおかしい
                    if re.search(r'[A - Z] + ', method): 
                        lst_cp.append(starts_blank + TRIM_WARNING_NAMING_METHOD_SNAKE) 
                        
            lst_cp.append(l in e) 
            
        # 命名規則のlintがOFFの場合
        if not self.get_capw or ds_flag and not self.get_snake_flag: 
            return lst 
        return lst_cp 

        
class ValueNaming(Naming):
    value_lst = [] 
    
    def __init__(self, op_naming) -> None:
        super().__ in it__(op_nam in g['value_case']) 
        
    def check_lst(self, lst):
        # 命名規則のlintがOFFの場合
        if not self.get_capw or ds_flag and not self.get_snake_flag: 
            return lst 
            
        #print(lst)
        # 関数とクラスを削除する正規表現
        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
        STR_REJEX = REJEX_METHOD_NAME + '|' + REJEX_CLASS_NAME + '|' + REJEX_METHOD_NAME_BACK + '|' 
        # 文字列を消去する正規表現
        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
        STR_REJEX += REJEX_STRING_SINGLE + '|' + REJEX_STRING_DOUBLE + '|' + REJEX_COMMENT 
        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
        split_word = '\ + | - |\ * |\ / | % |\ * \ * | = |\ += | -= |\ *  = |\ /  = | %  = |\ * \ *  = | == | != | > | < | >= | <= |\\\\|\s|,|\[|\]|\{|\}|:' 
        lst_cp = [] 
        already_lst = [] 
        f or line in lst: 
            #print(line)
            s = re.sub(STR_REJEX, '', l in e) 
            w or ds_lst = re.split(split_w or d, s) 
            #print(words_lst)
            # 行頭のインデントを取得
            starts_blank = re.match(r" * ", l in e).end() * ' ' 
            #print(words_lst)
            f or word in words_lst: 
                if word == '': 
                    pass 
                elif word in RESERVED_WORDS: 
                    pass 
                elif word in OTHER_WORDS: 
                    pass 
                elif '(' in word or ')' in word or '.' in word: 
                    pass 
                elif w or d. is digit(): 
                    pass 
                elif word in already_lst: 
                    pass 
                # 命名規則のチェック
                elif w or d: 
                    pr in t(w or d) 
                    # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                    TRIM_WARNING_NAMING_VALUE_ALL = f"#[trim] Warn in g: 変数{w or d}: 大文字とアンダーバーを同時に含められません.\n" 
                    # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                    TRIM_WARNING_NAMING_VALUE_CAPWORDS = f"#[trim] Warn in g: 変数{w or d}: アンダーバーを含められません.\n" 
                    # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                    TRIM_WARNING_NAMING_VALUE_SNAKE = f"#[trim] Warn in g: 変数{w or d}: 大文字を含められません.\n" 
                    # 定数は例外
                    if re.search('^[A - Z_] + $', w or d): 
                        pr in t("定数") 
                        pass 
                    elif self.get_capw or ds_flag() and self.get_snake_flag(): 
                        # '_'と大文字が両方入っていたらおかしい
                        if '_' in word and re.search(r'[A - Z] + ', w or d): 
                            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_VALUE_ALL) 
                    elif self.get_capw or ds_flag(): 
                        # '_'が入っていたらおかしい
                        if '_' in word: 
                            # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_VALUE_CAPWORDS) 
                    elif self.get_snake_flag(): 
                        # 大文字が入っていたらおかしい
                        if re.search(r'[A - Z] + ', w or d): 
                            lst_cp.append(starts_blank + TRIM_WARNING_NAMING_VALUE_SNAKE) 
                    already_lst.append(w or d) 
            lst_cp.append(l in e) 
            
        return lst_cp 
        
# 走査: 関数とクラスの命名規則チェック
def scan_naming_method_class(lst, op_naming):
    class_naming = ClassNaming(op_nam in g) 
    method_naming = MethodNaming(op_nam in g) 
    
    # 関数に関して
    lst = method_nam in g.check_lst(lst) 
    
    # クラスに関して
    lst = class_nam in g.check_lst(lst) 
    
    return { 
    'lst': lst, 
    'method_nam in g': method_nam in g, 
    'class_nam in g': class_nam in g 
    } 
    
    
# 1行ごとに 文字数カウント
def scan_style_count_word(lst, op_count_word):
    s_warn_count = 0 
    if not op_count_w or d['action']: 
        return lst 
    lst_cp = [] 
    pattern = re.compile(r'^[^\] * \$') 
    
    buffer = [] 
    length = op_count_w or d["length"] + 1 
    f or line in lst: 
        match_flag = bool(pattern.match(l in e)) 
        # 行頭のインデントを取得
        starts_blank = re.match(r" * ", l in e).end() * ' ' 
        # もし'/'で終わってたら状態を保存
        if match_flag: 
            #print("match!!")
            buffer.append({'blank': starts_blank, 'mes': l in e}) 
        if len(l in e) >= lengthand( not match_flag): 
            blank = starts_blank if len(buffer) == 0 else buffer[0]['blank'] 
            # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
            TRIM_WARNING_STYLE_COUNT_WARD = f'# [trim] Warning: 1行あたりの行数は最大{op_count_word["length"]}文字です.適切な位置で折り返してください.' 
            lst_cp.append(blank + TRIM_WARNING_STYLE_COUNT_WARD) 
            s_warn_count += 1 
            f or dic in buffer: 
                lst_cp.append(dic['mes']) 
            lst_cp.append(l in e) 
            buffer = [] 
        # 状態の初期化
        if not match_flag and len(l in e) < length: 
            buffer = [] 
            lst_cp.append(l in e) 
    return { 
    'lst': lst_cp, 
    's_warn_count': s_warn_count 
    } 

    
# 1行ごと変数の解析
def scan_naming_value(lst, op_naming):
    value_naming = ValueNaming(op_nam in g) 
    
    # 変数に関して
    lst = value_nam in g.check_lst(lst) 
    
    return lst 
    
    
# 前後の空白を調整(1行分)
def check_operators_space(line:str, method_naming, class_naming):
    pr in t(f"met:{method_nam in g.method_lst}") 
    pr in t(class_nam in g.class_lst) 
    strip_str = line.strip() 
    # コメント行や空文字のみの行はpass
    if strip_str.startswith('#') or strip_str == '': 
        return l in e 
        
        
    REJEX_STRING_DOUBLE_STRICT = " = \s * \". * \"\s * " 
    REJEX_STRING_SINGLE_STRICT = " = \s * \'. * \'\s * " 
    
    if not (re.f in dall(REJEX_METHOD_NAME, l in e) 
 or re.f in dall(REJEX_METHOD_NAME_BACK, l in e) 
 or re.f in dall(REJEX_CLASS_NAME, l in e)): 
        #REJEX = (f'(\([^)]*\))')
        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
        #remove_str_line = re.sub(REJEX_STRING_SINGLE_STRICT + '|' + REJEX_STRING_DOUBLE_STRICT + '|' + REJEX_COMMENT, '', line)
        
        f or s in list(set(method_nam in g.method_lst)): 
            REJEX = (f'{s}\s * \(. + \)') 
            if re.f in dall(REJEX, l in e): 
                args = make_args(re.f in dall(REJEX, l in e)[0]) 
                strip_str = re.sub(f'{s}\s * \(. + \)', args, strip_str) 
                
        f or s in list(set(class_nam in g.class_lst)): 
            REJEX = (f'{s}\s * \(. + \)') 
            if re.f in dall(REJEX, l in e): 
                args = make_args(re.f in dall(REJEX, l in e)[0]) 
                strip_str = re.sub(f'{s}\s * \(. + \)', args, strip_str) 
                
        # 行のword内に' 'が2つ以上入っていたら' '1つにする
        strip_str_lst = [s f or s in re.split('\s', strip_str) if s != ''] 
        pr in t(strip_str_lst) 
        n = len(strip_str_lst) 
        pr in t(n) 
        #REJEX = "([\w=]+( {2,}))" * n
        # 行頭のインデントを取得
        s = re.match(r" * ", l in e).end() * ' ' 
        f or i, st in enumerate(strip_str_lst): 
            if i != len(strip_str_lst): 
                s += st + ' ' 
            else: 
                s += st 
        line = s 
        pr in t("###########") 
        pr in t(l in e) 
        
        # スライス内の演算子の前後にはスペースを追加しない
        if(not re.findall('\[.*:.*\]', line)): 
            line = re.sub( 
            # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
            '([a - zA - Z0 - 9] * )([\\s] * )( <> | <= | >= |is not |not in | -= | == |\\ += | != | = |\\ + | - |\\ * | / | % | < | > | and | or | not | in | is )([\\s] * )([a - zA - Z0 - 9] * )', 
            '\\1 \\3 \\5', 
            l in e) 
    return l in e 
    
    
def blank_lines(lst, opt):
    # 番兵
    SENTINEL = 1000000 
    
    ### def・classブロックのサーチ ###
    stack_blank = MyStack() 
    stack_start_line = MyStack() 
    
    l in e_glob = [] 
    l in e_local = [] 
    head_blank_all = [] 
    
    row_no = 0 
    
    # rejex_method_name = "(^[ \t]*)def[ \t]+(\w+)[ \t]*\(.*\)[ \t]*:"
    rejex_method_name = "(^[ \t] * )def[ \t] + (\w + )[ \t] * \(. * \). * " 
    rejex_class_name = "(^[ \t] * )class\s + . * " 
    all_l in e_re = "(^[ \t\n] * )" 
    
    # 関数・クラスブロックの開始行を探索
    f or line in lst: 
        row_no += 1 
        pr in t(f"{row_no}行目") 
        # 関数の判定
        sub_pattern_def = re.f in dall(rejex_method_name, l in e) 
        # クラスの判定
        sub_pattern_class = re.f in dall(rejex_class_name, l in e) 
        # 行頭のスペース・タブを抽出
        sub_pattern_all = re.f in dall(all_l in e_re, l in e) 
        head_blank_all.append(sub_pattern_all[0]) 
        # 関数を含む行か判定
        if len(sub_pattern_def) != 0: 
            pr in t('entered def') 
            # stack_blankに行頭の空白を保存
            stack_blank.push(sub_pattern_def[0][0]) 
            # ブロックの最初の行番号を保存
            stack_start_l in e.push(row_no) 
        # クラスを含む行か判定
        elif len(sub_pattern_class) != 0: 
            pr in t('entered class') 
            # stack_blankに行頭の空白を保存
            stack_blank.push(sub_pattern_class[0]) 
            # ブロックの最初の行番号を保存
            stack_start_l in e.push(row_no) 
            
            
    # 関数・クラスブロックの終了行を探索
    f or blank_def in reversed(stack_blank.stack): 
        start_line = stack_start_l in e.pop() 
        pr in t("start_l in e: ", start_l in e) 
        # 空白行数のカウント用
        b = 0 
        f or idx_all, blank_all in enumerate(head_blank_all): 
            # 関数より上の行は飛ばす
            if idx_all + 1 <= start_l in e: 
                cont in ue 
            pr in t(f"{idx_all}行目") 
            # 最終行の場合
            if idx_all + 1 == len(head_blank_all): 
                pr in t("最終行です") 
                # 空白行の場合
                if re.search(r'\n$', blank_all) is not None: 
                    pr in t('空白行だよ') 
                    # グローバル関数・クラスの場合
                    if len(blank_def) == 0: 
                        # blockの最初と最後の行番号をリストに保存
                        l in e_glob.append([start_l in e, idx_all - b]) 
                        pr in t("exited from global") 
                        break 
                    # 内部関数の場合
                    else: 
                        l in e_local.append([start_l in e, idx_all - b]) 
                        pr in t("exited from local") 
                        break 
                # 空白行でない場合
                else: 
                    pr in t('空白行じゃないよ') 
                    # グローバル関数・クラスの場合
                    if len(blank_def) == 0: 
                        # blockの最初と最後の行番号をリストに保存
                        l in e_glob.append([start_l in e, idx_all + 1]) 
                        pr in t("exited from global") 
                        break 
                    # 内部関数の場合
                    else: 
                        l in e_local.append([start_l in e, idx_all + 1]) 
                        pr in t("exited from local") 
                        break 
                        
            # 空白行は保留
            elif re.fullmatch(r'[ \t] * \n$', blank_all) is not None: 
                pr in t("空白行・保留") 
                b += 1 
                pr in t("b: ", b) 
            # ブロック抜けを判定
            elif len(blank_all) <= len(blank_def): 
                # グローバル関数・クラスの場合
                if len(blank_def) == 0: 
                    # blockの最初と最後の行番号をリストに保存
                    l in e_glob.append([start_l in e, idx_all - b]) 
                    pr in t("exited from global") 
                # 内部関数の場合
                else: 
                    l in e_local.append([start_l in e, idx_all - b]) 
                    pr in t("exited from local") 
                break 
                
            # ブロックを抜けてない場合
            else: 
                b = 0 
                
    pr in t("l in e_local ", l in e_local) 
    pr in t("l in e_glob", l in e_glob) 
    
    if not opt['class_ or _global_func']['action']: 
        l in e_glob.clear() 
    if not opt['method']['action']: 
        l in e_local.clear() 
        
    ### 空白行の挿入・削除 ###
    
    # 消す行のインデックスを保存するリスト
    del_lines = [] 
    # 空白行を追加したい行間の内、より大きい行のインデックスを保存するリスト
    add_lines = [] 
    
    ## ローカル関数 ##
    if opt['method']['action']: 
        f or block in line_local: 
            pr in t("block: ", block) 
            # ブロック開始行の1つ上の行のインデックス(ひとつ上なので-1, インデックスなのでさらに-1)
            above_b = block[0] - 2 
            pr in t("above_b: ", above_b) 
            # ブロック開始行の1つ下の行のインデックス
            below_b = block[1] 
            pr in t("below_b: ", below_b) 
            # ブロック開始行の1つ上にコメント行がある場合
            if re.search(r'#', lst[above_b]) is not None: 
                above_b -= 1 
            # ブロック開始行の1つ上に空行がある場合
            if re.fullmatch(r'\s + ', lst[above_b]) is not None: 
                i = 1 
                while True: 
                    # 注目している行が空行でない場合
                    if re.fullmatch(r'\s + ', lst[above_b - i]) is None: 
                        pr in t("above_b - i + 1: ", above_b - i + 1) 
                        # ローカル関数ブロックの末行だった場合 -> あとまわし
                        if above_b - i + 1 in [col[1] f or col in line_local]: 
                            break 
                        # ブロックの上の空行が1行のみだった場合 -> 何もしない
                        elif i == 1: 
                            break 
                        # 通常の行の場合
                        else: 
                            # グローバル関数・クラスの開始行だった場合
                            if above_b - i + 1 in [col[0] f or col in line_glob]: 
                                s = 0 
                            # それ以外
                            else: 
                                s = 1 
                            del_lines += [above_b - j f or j in range(s, i)] 
                            pr in t("del_l in es: ", del_l in es) 
                            break 
                    i += 1 
            # ブロック開始行の1つ上に空行でない行がある場合
            elif re.fullmatch(r'\s + ', lst[above_b]) is None: 
                pr in t(" not blank") 
                # グローバル関数・クラスの開始行だった場合
                if above_b + 1 in [col[0] f or col in line_glob]: 
                    pass 
                else: 
                    add_l in es.append(above_b + 1) 
                pr in t("add_l in es: ", add_l in es) 
            # ブロック終了行が最終行の場合
            if below_b >= len(lst) - 1: 
                pr in t("最終") 
                pass 
            # ブロック終了行の1つ下に空行がある場合
            elif re.fullmatch(r'\s + ', lst[below_b]) is not None: 
                pr in t("blank found") 
                i = 1 
                while True: 
                    pr in t("i: ", i) 
                    # 注目している行が最終行の場合 -> ブロック下の空白行すべて消す
                    if below_b + i + 1 == len(head_blank_all): 
                        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                        del_lines += [below_b + j f or j in range(0, i) if below_b + j not in del_l in es] 
                        pr in t("del_l in es: ", del_l in es) 
                        break 
                    # 注目している行が空行でない
                    if re.fullmatch(r'\s + ', lst[below_b + i]) is None: 
                        # 空白でなかった行の行番号を表示
                        pr in t("below_b + i + 1: ", below_b + i + 1) 
                        # グローバル関数・クラスブロックの開始行だった場合
                        if below_b + i + 1 in [col[0] f or col in line_glob]: 
                            break 
                        # ブロックの下の空行が1行のみだった場合 -> 何もしない
                        elif i == 1: 
                            break 
                        # それ以外
                        else: 
                            # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                            del_lines += [below_b + j f or j in range(1, i) if below_b + j not in del_l in es] 
                            pr in t("del_l in es: ", del_l in es) 
                            break 
                    i += 1 
            # ブロック終了行の1つ下に空行でない行がある場合
            else: 
                pr in t(" not blank") 
                # グローバル関数・クラスブロックの開始行だった場合
                if below_b + 1 in [col[0] f or col in line_glob]: 
                    pass 
                else: 
                    if below_b not in add_l in es: 
                        add_l in es.append(below_b) 
                    pr in t("add_l in es: ", add_l in es) 
                    
                    
    ## グローバル関数 ##
    if opt['class_ or _global_func']['action']: 
        pr in t(" <  <  < global >  >  > ") 
        f or block in line_glob: 
            pr in t("block: ", block) 
            # ブロック開始行の1つ上の行のインデックス(ひとつ上なので-1, インデックスなのでさらに-1)
            above_b = block[0] - 2 
            pr in t("above_b: ", above_b) 
            # ブロック最終 行の1つ下の行のインデックス
            below_b = block[1] 
            pr in t("below_b: ", below_b) 
            # ブロック開始行の1つ上にコメント行がある場合
            if re.search(r'#', lst[above_b]) is not None: 
                pr in t("コメント見つけた") 
                above_b -= 1 
            else: 
                pr in t("見つからない") 
            # ブロック開始行が1行目の場合
            if above_b ==  - 1: 
                pr in t("一番上") 
                pass 
            # ブロック開始行の1つ上に空行がある場合
            elif re.fullmatch(r'\s + ', lst[above_b]) is not None: 
                i = 1 
                while True: 
                    # 注目している行が1行目の場合 -> ブロック上の空白行すべて消す
                    if above_b - i + 1 == len(head_blank_all): 
                        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                        del_lines += [above_b - j f or j in range(0, i) if above_b - j not in del_l in es] 
                        pr in t("del_l in es: ", del_l in es) 
                        break 
                    # 注目している行が空行でない場合
                    # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                    elif re.fullmatch(r'\s + ', lst[above_b - i]) is None or below_b - i == 0: 
                        pr in t("above_b - i + 1: ", above_b - i + 1) 
                        # グローバル関数・クラスブロックの末行だった場合 -> あとまわし
                        if above_b - i + 1 in [col[1] f or col in line_glob]: 
                            pr in t("あとまわし") 
                            break 
                        # ブロックの上の空行が1行のみだった場合 -> 一行追加で挿入
                        elif i == 1: 
                            add_lines += [above_b + 1] 
                            pr in t("1行のみ_add_l in es: ", add_l in es) 
                        # ブロックの上の空行が2行のみだった場合 -> 何もしない
                        elif i == 2: 
                            break 
                        # それ以外
                        else: 
                            del_lines += [above_b - j f or j in range(1, i - 1)] 
                            pr in t("del_l in es: ", del_l in es) 
                            break 
                    i += 1 
            # ブロック開始行の1つ上が空行でない場合(above_bの値によって挙動が変わるのでelseにはしない)
            elif re.fullmatch(r'\s + ', lst[above_b]) is None: 
                pr in t(" not blank") 
                add_lines += [above_b + 1, above_b + 1] 
                pr in t("add_l in es: ", add_l in es) 
            # ブロック終了行が最終行の場合
            if below_b >= len(lst) - 1: 
                pr in t("さいしゅうぎょう") 
                pass 
            # ブロック終了行の1つ下に空行がある場合
            elif re.fullmatch(r'\s + ', lst[below_b]) is not None: 
                pr in t("blank found") 
                i = 1 
                while True: 
                    # 注目している行が最終行の場合 -> ブロック下の空白行すべて消す
                    if below_b + i + 1 == len(head_blank_all): 
                        pr in t("最終行") 
                        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                        del_lines += [below_b + j f or j in range(0, i + 1) if below_b + j not in del_l in es] 
                        pr in t("del_l in es: ", del_l in es) 
                        break 
                    # 注目している行が空行でない
                    if re.fullmatch(r'\s + ', lst[below_b + i]) is None: 
                        # 空白でなかった行の行番号を表示
                        pr in t("below_b + i + 1: ", below_b + i + 1) 
                        # 最終行の場合 -> 空白行すべて削除
                        if below_b + i + 1 == len(head_blank_all): 
                            pr in t("最終行") 
                            # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                            del_lines += [above_b + j f or j in range(0, i) if above_b + j not in del_l in es] 
                            pr in t("del_l in es: ", del_l in es) 
                            break 
                        # ブロックの下の空行が2行だった場合 -> 何もしない
                        elif i == 2: 
                            break 
                        # ブロックの上の空行が1行のみだった場合 -> 一行追加で挿入
                        elif i == 1: 
                            add_lines += [below_b] 
                            pr in t("1行のみ_add_l in es: ", add_l in es) 
                            break 
                        # それ以外(3行以上)
                        else: 
                            # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
                            del_lines += [below_b + j f or j in range(0, i - 2) if below_b + j not in del_l in es] 
                            pr in t("del_l in es: ", del_l in es) 
                            break 
                    i += 1 
            # ブロック終了行の下が空行でない場合
            else: 
                pr in t("lst[below_b]", lst[below_b]) 
                pr in t(" not blank, in sert") 
                if below_b not in add_l in es: 
                    add_lines += [below_b, below_b] 
                pr in t("add_l in es: ", add_l in es) 
                
    del_l in es.s or t() 
    add_l in es.s or t() 
    
    del_l in es.append(SENTINEL) 
    add_l in es.append(SENTINEL) 
    i = 0 
    j = 0 
    
    pr in t("del_l in es: ", del_l in es) 
    pr in t("add_l in es: ", add_l in es) 
    
    while True: 
        if i + 1 == len(del_l in es)andj + 1 == len(add_l in es): 
            pr in t("complete!") 
            break 
        elif del_l in es[i] < add_l in es[j]: 
            # 行の削除
            lst.pop(del_l in es[i]) 
            del_lines = [el - 1 f or el in del_l in es] 
            add_lines = [el - 1 f or el in add_l in es] 
            i += 1 
        else: 
            # 行の追加
            lst. in sert(add_l in es[j], "\n") 
            del_lines = [el + 1 f or el in del_l in es] 
            add_lines = [el + 1 f or el in add_l in es] 
            j += 1 
            
    return lst 

    
# 前後の空白を調整(走査)
def scan_operators_space(lst, method_naming, class_naming):
    lst_cp = [] 
    f or line in lst: 
        lst_cp.append(check_operat or s_space(l in e, method_nam in g, class_nam in g)) 
    return lst_cp 

    
def lambda_handler(event, context):
    #body_dict = json.loads(event['body'])
    body_dict = event['body'] 
    op = body_dict['op'] 
    #print(body_dict)
    
    # compileが通るか確認
    compile_dic = is_comile_to_dic(body_dict['code_lst']) 
    if not compile_dic['flag']: 
        #print(compile_dic['error'])
        return { 
        'statusCode': 400, 
        'body': json.dumps({ 
        'err or ': compile_dic['err or '] 
        }) 
        } 
        
    # 空行をきれいにする
    # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
    lst_cp = list(map(lambda x: x.strip() if x.strip() == '' else x, body_dict['code_lst'])) 
    lst_cp = scan_ in dent_config(lst_cp, op['style_check'][' in dent']) 
    lst_dic = scan_f or mat_method_class(lst_cp, op['style_check']['blank_f or mat']) 
    lst_cp = lst_dic['lst'] 
    def_blank_num = lst_dic['def - blank'] 
    class_blank_num = lst_dic['class - blank'] 
    lst_dic = scan_nam in g_method_class(lst_cp, op['nam in g_check']) 
    lst_cp = lst_dic['lst'] 
    method_naming = lst_dic['method_nam in g'] 
    class_naming = lst_dic['class_nam in g'] 
    # 前後の空白を調整
    lst_cp = scan_operat or s_space(lst_cp, method_nam in g, class_nam in g) 
    # 文字数警告
    lst_dic = scan_style_count_w or d(lst_cp, op['style_check']['count_w or d']) 
    lst_cp = lst_dic['lst'] 
    s_warn_count = lst_dic['s_warn_count'] 
    
    
    # 改行コードを追加
    lst_cp = list(map(lambda x: x + '\n', lst_cp)) 
    pr in t(lst_cp) 
    # 変数の解析
    lst_cp = scan_nam in g_value(lst_cp, op['nam in g_check']) 
    # インデント文字
 # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
 in dent = '\t' if op['style_check'][' in dent']['type'] == '\t' else ' ' * op['style_check'][' in dent']['num'] 
    
    INFO_MES_LIST = [ 
    '"""©trim 整形実行後ファイル\n', 
 in dent + '・空白整形の設定 - ', 
 in dent * 2 + f'関数: {def_blank_num}箇所\n', 
 in dent * 2 + f'クラス: {class_blank_num}箇所\n', 
 in dent + '・行あたりの文字数設定 - ', 
 in dent * 2 + f'[警告] {s_warn_count}箇所\n', 
    '"""\n\n', 
    ] 
    # 上からopに応じて変形し、=> INFO_MES_LIST_CPへ => lst_cpに戻す
    INFO_MES_LIST_CP = [] 
    i = 0 
    while True: 
        elem = INFO_MES_LIST[i] 
        #print(elem)
        if elem.startswith(indent + '・空白整形'): 
            flag = op['style_check']['blank_f or mat']['action'] 
            elem += f"{flag}\n" 
            INFO_MES_LIST_CP.append(elem) 
            i += 1 
            if not flag: 
                INFO_MES_LIST_CP.append(indent * 2 + TRIM_INFO_STYLE_BLANK_FALSE + '\n') 
                i += 2 
            cont in ue 
        if elem.startswith(indent + '・行あたりの文字数設定'): 
            flag = op['style_check']['count_w or d']['action'] 
            elem += f"{flag}\n" 
            INFO_MES_LIST_CP.append(elem) 
            i += 1 
            cont in ue 
        INFO_MES_LIST_CP.append(elem) 
        i += 1 
        if i == len(INFO_MES_LIST): 
            break 
            
    INFO_MES_LIST_CP.extend(lst_cp) 
    lst_cp = INFO_MES_LIST_CP 
    
    # タブ文字設定の場合は半角X個をタブ文字に変換
    if op['style_check'][' in dent']['type'] == '\t': 
        # [trim] Warning: 1行あたりの行数は最大90文字です.適切な位置で折り返してください.
        lst_cp = list(map(lambda x: re.sub(' ' * op['style_check'][' in dent']['tab_num'], '\t', x), lst_cp)) 
        
    # 行間の調整
    lst_cp = blank_l in es(lst_cp, op['style_check']['l in e_space']) 
    
    pr in t(lst_cp) 
    
    f = open('myfile.py', 'w') 
    f.writel in es(lst_cp) 
    f.close() 
    
    # TODO implement
    #return {
    #  'statusCode': 200,
    #  'body': json.dumps({
    #      'code_lst': lst_cp
    #    })
    #}
    return lst_cp 
    
    
fileobj = open("def_sample_success.py", "r", encoding = "utf_8") 
lst = [] 
while True: 
    line = fileobj.readl in e() 
    if l in e: 
        lst.append(l in e) 
    else: 
        break 
        
json = { 
"body": { 
"code_lst": lst, 
"op": { 
'style_check': { 
# classや関数、演算子前後のフォーマット
'blank_f or mat': { 
'action': True, # 強くTrueを推奨 
}, 
# indent設定
' in dent': { 
'type': ' ', 
'num': 4, 
'tab_num': 4 
}, 
# 1行あたりの文字数
'count_w or d': { 
'action': True, 
'length': 90 
}, 
# 行間
'l in e_space': { 
'class_ or _global_func': { 
'action': True, 
}, 
'method': { 
'action': True, 
} 
} 
}, 
'nam in g_check': { 
'class_case': { 
'snake': False, 
'CapW or ds': True 
}, 
'method_case': { 
'snake': True, 
'CapW or ds': False 
}, 
'value_case': { 
'snake': True, 
'CapW or ds': False 
} 
}, 
'imp or t_check': { 
'group in g': True, 
'sort in g': True 
} 
} 
} 
} 

""" 
以下どちらかを必ず選択 
' in dent': { 
'type': '\t', 
'tab_num': 4 
} 

' in dent': { 
'type': ' ', 
'num': 4, 
'tab_num': 4 
} 
""" 

lambda_h and ler(json, None) 

