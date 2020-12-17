import wlan_pcap
import os
import access_manage
import db_func
import sys
import time

class pcap_analyzer:
    def __init__(self):
        # パケット解析ライブラリ
        self.wp = wlan_pcap.wlan_pcap()

        # データベースへの接続
        self.db = db_func.db_func()

        # アクセス管理するライブラリ
        self.am = access_manage.access()


    def access_update(self):
        # MACアドレスからユーザを検索
        mac_addr_list = list(self.access_data.keys())

        field_name = "*"
        table_name = "user"
        wh_field = "mac_addr"

        # SQLの構文ではリスト[]ではなくタプル()に注意
        if len(mac_addr_list) == 1:
            value = mac_addr_list[0]
            user_list = self.db.get_where(field_name, table_name, wh_field, value)
        elif len(mac_addr_list) == 0:
            print("Wi-Fiログから誰もいないと判断したよ")
            sys.exit(0)
        else:
            mac_addr_list = tuple(mac_addr_list)
            where_column = "mac_addr"
            user_list = self.db.where_list(where_column ,mac_addr_list)

        time_list = list(self.access_data.values())

        print(user_list)

        # マッチした各ユーザの入退室を更新
        user_num = 0
        for user in user_list:
            user_dic = {
                    "id" : user[0],
                    "full_name" : user[3],
                    "student_id" : user[1],
                    "token" : user[4],
                    "time" : self.access_data[user[6]].strftime('%Y-%m-%d %H:%M:%S')
            }

            self.am.access_manage(user_dic, True)
            user_num += 1


    def get_pcap(self, path):
        # tcpdumpの仕様を使用したループ
        # while True:
        file_list = self.wp.get_file(path)
        print(file_list)
        if len(file_list) >= 2:
            return file_list
        else:
            print("既定のpcapfile数を下回ってます。")
            sys.exit(1)


    def main(self):
        # スタート
        # start = time.time()

        # 処理対象のpcapファイルを取得する
        path = "/home/pi/pcap"
        file_list = self.get_pcap(path)
        pcap_file = os.path.join(path, file_list[0])

        # 入退室管理を更新する
        self.access_data = self.wp.pcap_reader(pcap_file, "test")
        self.access_update()

        # 処理対象のpcapファイルを削除する
        self.wp.delete_file(pcap_file)

        # エンド
        # elapsed_time = time.time() - start
        # print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

if __name__ == "__main__":
    pa = pcap_analyzer()
    pa.main()