import line_func
import db_func
import access_manage
import time
import datetime
from datetime import datetime as dt

class notify:
    def __init__(self):
        # データベースへの接続
        self.db = db_func.db_func()

        # LINE機能を使うためのインスタンス
        self.line = line_func.line_func()

        # 入退室情報を管理機能
        self.access = access_manage.access()


    def access_user_search(self):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.date.today()

        field_name = "*"
        wh_field = "date"

        # 今日の入退室記録がある人を検索
        access_info = self.db.get_access_info(field_name, wh_field ,today)

        self.access_info = access_info
        access_info.sort()

        print(access_info)

    def get_user_info(self):
        user_id_list = []
        # ユーザidを取り出す
        for value in self.access_info:
            user_id = value[0]
            user_id_list.append(user_id)
            
            user_id_list.sort()

        # sqlの構文では, リスト:[] ではなく タプル:()
        if len(user_id_list) == 1:
            user_id_list = 1
        else:
            user_id_list = tuple(user_id_list)

        user_info = self.db.get_user_list(user_id_list)

        self.user_info = user_info
        print(user_info)


    def form_info_create(self):
        self.form_info = []

        for (user, access) in zip(self.user_info, self.access_info):
            date = str(access[1]) + "%20"
            entry_time = str(access[2])[11:16]
            exit_time = str(access[3])[11:16]

            access_time = date + entry_time + "~" +exit_time
            print(access_time)

            form_dic = {
                    "full_name" : user[1],
                    "student_id": user[2],
                    "token" : user[3],
                    "access_time" : access_time
            }

            self.form_info.append(form_dic)
            print(self.form_info)

    def line_push(self):
        self.line.line_push(self.form_info)

    def line_push_pre(self):
        self.line.line_push_pre(self.form_info)

if __name__ == "__main__":
    notify = notify()
    notify.access_user_search()
    notify.get_user_info()
    notify.form_info_create()
    # notify.line_push()
