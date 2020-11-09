import db_func
import requests

class line_func:
    def __init__(self):
        # LINE通知APIのエンドポイント
        self.line_notify_api = 'https://notify-api.line.me/api/notify'

        # Googleフォームの情報
        self.url = "https://docs.google.com/forms/d/e/1FAIpQLSf-ZVJL-6nDNftQTqkWdvncSpnYwObAXZaObIuB6_m-WWhmzw/viewform?"
        self.entry = {
            "name": 2005620554,
            "id": 1045781291,
            "time": 1065046570
        }

    
    def line_push_test(self, msg):
        headers = {'Authorization': f'Bearer {self.token}'}
        data = {'message': f'message: {msg}'}
        status = requests.post(self.line_notify_api, headers = headers, data = data)
        print(status)


    def line_push(self, user_dic, access_time):

        full_name = user_dic["full_name"]
        student_id = user_dic["student_id"]
        access_time = "2020/11/09%2012:00~13:00"
        token = user_dic["token"]

        name = "entry.{0}={1}&".format(self.entry["name"], full_name)
        id = "entry.{0}={1}&".format(self.entry["id"], student_id)
        time = "entry.{0}={1}".format(self.entry["time"], access_time)

        url = self.url + name + id + time

        print(url)

        headers = {'Authorization': f'Bearer {token}'}
        data = {'message': f'message: {url}'}
        status = requests.post(self.line_notify_api, headers = headers, data = data)

        print(status)
        
        
    def main(self):
        pass


if __name__ == "__main__":
    line = line_func()

