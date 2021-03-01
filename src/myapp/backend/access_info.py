import db_module
import time
import datetime
from datetime import datetime as dt

class access:
    def __init__(self):
        self.db = db_module.db_func()


    def access_user_search(self):
        

        # 現在時刻を取得
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.date.today()

        field_name = "*"
        wh_field = "date"

        # 今日の入退室記録がある人を検索
        access_info = self.db.get_access_info(field_name, wh_field ,today)

        self.access_info = access_info
        access_info.sort()
        
        

        # ユーザ名を抽出するためのクエリ
        field_name = "name"
        table_name = "user"
        wh_field = "id"

        # ユーザのアクセス情報のリスト
        access_list = []

        for user in access_info:
            # 各ユーザのアクセス情報を保持する辞書
            access_dict = {}

            user_id = user[0]

            # in_time = user[2].strftime('%Y-%m-%d %H:%M:%S')
            in_time = user[2].strftime('%H:%M:%S')

            if user[3] != None:
                state = self.check_state(user[3])
                out_time = user[3].strftime('%H:%M:%S')
            else:
                out_time = "---"
                state = "入室中"
                

            user_name = self.db.get_where(field_name, table_name, wh_field, user_id)[0]

            access_dict["in_time"] = in_time
            access_dict["out_time"] = out_time
            access_dict["name"] = user_name
            access_dict["access"] = state

            access_list.append(access_dict)

        return access_list


    def check_state(self, out_time):
        # 現在時刻を取得
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        now_dt = dt.strptime(now, '%Y-%m-%d %H:%M:%S')

        out = out_time.strftime('%Y-%m-%d %H:%M:%S')
        out_dt = dt.strptime(out, '%Y-%m-%d %H:%M:%S')

        # 現在時刻と退室時間を比較
        td = now_dt - out_time
        # 1000秒経過していたら退室と判定
        if td.seconds >= 1000:
            state = "退室済"
        else:
            state = "入室中"

        return state