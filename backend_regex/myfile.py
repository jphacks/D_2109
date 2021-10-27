"""©trim 整形実行後ファイル
    ・空白整形の文字数設定 - True
        関数: 6箇所
        クラス: 5箇所
    ・行あたりの文字数設定 - True
        [警告] 1箇所
"""

a=3
v=2

def a(a, b, c=2) -> int:
    # [trim]Warning: 1行あたりの行数は最大80文字です.適切な位置で折り返してください.
    Customer.\
    objects.\
    filter(delete_flag=False).order_by('id')[:10].values('id', 'name', 'name_furigana', 'phone', 'mail', 'gender', 'customer_type__name', 'withdrawal_date', 'status', 'birth_date', 'active_flag', 'category_name',)
    pass

def add_box(a, b, c=3):
    ab = 2
    a = 3
    method = a(ab,a)
    def aaaa():
        return ab
    return  ab



# [trim] Warning: クラス名に大文字は含められません.
class PermissionMixin:
    def __init__(self) -> None:
        pass
    def a(self):
        pass

# [trim] Warning: クラス名に大文字は含められません.
class BaseUser():
    def __init__(self) -> None:
        pass
    pass

# [trim] Warning: クラス名に大文字は含められません.
class User(BaseUser, PermissionMixin):
    name = "aaaa"

    def __init__(self) -> None:
        super().__init__()

    # [trim] Warning: 関数名に大文字は含められません.
    def getName(self):
        return self.name
