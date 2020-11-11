import db_func
import requests

class line_func:
    def __init__(self):
        # LINE通知APIのエンドポイント
        self.line_notify_api = 'https://notify-api.line.me/api/notify'

        # Googleフォームの情報
        # self.url = "https://docs.google.com/forms/d/e/1FAIpQLSf-ZVJL-6nDNftQTqkWdvncSpnYwObAXZaObIuB6_m-WWhmzw/viewform?"
        # self.entry = {
        #     "name": 2005620554,
        #     "id": 1045781291,
        #     "time": 1065046570
        # }

        self.url = "https://docs.google.com/forms/d/e/1FAIpQLSe2DgXoLpk_eTF6tRuUSNpciWYgyl02TWsGlhp-HbrxPkxvrw/viewform?"
        self.entry = {
            "name": 208832475,
            "id": 913668226,
            "time": 1243542068
        }

    
    def line_push_test(self, msg):
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {'message': f'message: {msg}'}
        status = requests.post(self.line_notify_api, headers = headers, data = data)
        print(status)


    def line_push(self, user_list):
        # ユーザごとのURLを保持
        url_list = []

        for user_dic in user_list:
            # ユーザ情報の取得
            full_name = user_dic["full_name"]
            student_id = user_dic["student_id"]
            access_time = user_dic["access_time"]
            token = user_dic["token"]

            # GoogleフォームのURLを生成
            name = "entry.{0}={1}&".format(self.entry["name"], full_name)
            id = "entry.{0}={1}&".format(self.entry["id"], student_id)
            time = "entry.{0}={1}".format(self.entry["time"], access_time)

            url = self.url + name + id + time

            # ポストする
            headers = {'Authorization': f'Bearer {token}'}
            data = {'message': f'{url}'}
            status = requests.post(self.line_notify_api, headers = headers, data = data)

            print(status)

    def detect_push(self, user_dic, access_flag):
        token = user_dic["token"]
        # 入室か退室かでmsgを分ける
        if access_flag == True:
            msg = "入室記録作成しましたよ"
        else:
            msg = "お疲れ！退室記録更新しとくわ"
        # 検出されたことをポストする
        headers = {'Authorization': f'Bearer {token}'}
        data = {'message': f'{msg}'}
        status = requests.post(self.line_notify_api, headers = headers, data = data)

        print(status)


    def main(self):
        pass


if __name__ == "__main__":
    line = line_func()
