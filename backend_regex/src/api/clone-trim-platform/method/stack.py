# スタックの定義(by 刀祢)
class Stack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        result = self.stack[-1]  # 末尾の要素を変数に取り出す
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する


# 多機能スタック
class InitDisplayStack(Stack):
    def __init__(self, n):
        self.stack = [n]
    def get_top(self):
        return self.stack[-1]
    def get_reverse_lst(self):
        return reversed(self.stack)
