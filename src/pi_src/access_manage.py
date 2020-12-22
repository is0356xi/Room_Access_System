import db_func
import time
import datetime
from datetime import datetime as dt

class access:
    def __init__(self):
        # データベースへの接続
        self.db = db_func.db_func()


    def access_manage(self, match_user):
        # 現在時刻を取得
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        today = datetime.date.today()

        # 補正時刻
        min_time = time.strftime('%Y-%m-%d 09:00:32')
        max_time = time.strftime('%Y-%m-%d 21:58:12')

        # クエリに含める情報の設定
        field_name = "*"
        table_name = "access"
        wh_field = "id"
        user_id = match_user["id"]

        # 入退室情報があるかどうか検索
        access_info = self.db.get_where(field_name, table_name, wh_field ,user_id)
        # 入室記録の日付を取得
        for value in access_info:
            # 現在時刻と入室記録の日付が一致するまでループ
            date = value[1].strftime('%Y-%m-%d')
            if str(date) == str(today):
                break

        # 入退室に関する記録がない場合
        if len(access_info) == 0:

            dt_min = dt.strptime(min_time, '%Y-%m-%d %H:%M:%S')
            dt_now = dt.strptime(now, '%Y-%m-%d %H:%M:%S')
            if dt_min > dt_now:
                now = dt_min
            
            self.db.access_info_manage(user_id, today, now ,True)
            print("")
            print("入退室記録なし")

            return True

        # 入室記録はあるが日付が変わっている場合
        elif str(date) != str(today):
            self.db.access_info_manage(user_id, today, now ,True)
            print("")
            print("今日はまだ入室してないと思います。")

            return True

        #　入退室記録があり、退出時間を更新する場合
        else:
            dt_max = dt.strptime(max_time, '%Y-%m-%d %H:%M:%S')
            dt_now = dt.strptime(now, '%Y-%m-%d %H:%M:%S')
            if dt_max < dt_now:
                now = max_time

            self.db.access_info_manage(user_id, today, now)
            print("")
            print("退出記録更新")

            return False


    def exit_manage(self):
        # クエリに含める情報の設定
        field_name = "exit_time"
        wh_field = "date"
        today = datetime.date.today()

        access_info = self.db.get_access_info(field_name, wh_field ,today)
        
        for value in access_info:
            if value[0] == None:
                print("何か忘れてない？")


if __name__ == "__main__":
    pass