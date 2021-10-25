a=3
v=2

def a():
	pass


# [trim] 警告: 関数名に大文字は含められません.
def Add_box(a, b, c=3):
	ab = 2
	a = 3
	def aaaa():
		return ab
	return  ab



# [trim] 警告: クラス名に大文字は含められません.
class PermissionMixin:
	def __init__(self) -> None:
		pass
	def a(self):
		pass

# [trim] 警告: クラス名に大文字は含められません.
class BaseUser():
	def __init__(self) -> None:
		pass
	pass

# [trim] 警告: クラス名に大文字は含められません.
class User(BaseUser, PermissionMixin):
	name = "aaaa"

	def __init__(self) -> None:
		super().__init__()

	# [trim] 警告: 関数名に大文字は含められません.
	def getName(self):
		return self.name
