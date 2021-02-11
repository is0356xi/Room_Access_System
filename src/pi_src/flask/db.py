import sys
sys.path.append('../')

from db_src import db_func

class DB():
    def __init__(self):
        self.db = db_func.db_func()
        print("DB呼び出し")

    def sign_up(self, data):
        self.data = data
        self.db.create_user(*data)

        print("DB登録処理")