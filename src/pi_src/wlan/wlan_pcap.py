# -*- coding: utf-8 -*-
import os
import subprocess
from scapy.all import *
import sys
import datetime as dt
import db_func
import datetime as dt


class wlan_pcap:
    def __init__(self):
        # データベースへの接続
        self.db = db_func.db_func()

    def get_file(self, path):
        # pathで指定されるディレクトリに含まれるファイルをリスト化する
        files = os.listdir(path)
        file_list = [f for f in files if os.path.isfile(os.path.join(path, f))]

        # 順不同なのでソートする
        file_list = sorted(file_list)

        return file_list

    def delete_file(self, file_path):
        res = subprocess.run(
            ["rm", "-rf", file_path]
        )

    # def read_pcap(self, filename, output_file):
    #     #　ファイルが存在しない場合
    #     if not os.path.isfile(filename):
    #         print("{0} does not exits".format(filename))
    #         sys.exit(-1)
    #     else:
    #         print("successed read: {0}".format(filename))

    #     # パケットキャプチャファイルの読み込み
    #     print(dt.datetime.now())
    #     packets = rdpcap(filename)
    #     print(dt.datetime.now())
        
    #     count = 0

    #     # MACアドレスをキーとした辞書を作成する
    #     access_data = {}

    #     # MACアドレスのリストを取得
    #     column_name = "mac_addr"
    #     table_name = "user"
    #     addr_list = self.get_addr_list(column_name, table_name)

    #     # 1パケットずつ処理する
    #     for packet in packets:
    #         try:
    #             # 802.11レイヤーのパケットのみを処理
    #             if packet.haslayer(Dot11) and packet.type==2: # タイプ2 = Data Frames
    #                 # print("packet No.{0}".format(count))
    #                 # flagの特定部分を抽出
    #                 DS_flag = packet.FCfield & 0x3
    #                 # DS(Distribution System)に向かうかどうかを判定
    #                 toDS = DS_flag & 0x01 != 0
    #                 fromDS = DS_flag & 0x2 != 0

    #                 if toDS and not fromDS:
    #                     # MACアドレスが登録されているかどうか
    #                     if packet.addr2 in addr_list:
    #                         # 送信者(=スマホ)のMACアドレスを格納
    #                         TA = packet.addr2
    #                         # パケットの到着時間を取得
    #                         packet_time = dt.datetime.fromtimestamp(packet.time, dt.timezone(dt.timedelta(hours=9)))

    #                         # print(TA, packet_time)
    #                         access_data[TA] = packet_time
                        

    #                 # DS向けかどうかで処理を分ける (Null functionはtoDSのみっぽい)
    #                 # if toDS and not fromDS:
    #                 #     print("*** From STA to DS via AP ***")
    #                 #     print("Receiver Address: {0}".format(packet.addr1))
    #                 #     print("Transmitter Address: {0}".format(packet.addr2))
    #                 #     print("Destination Address: {0}".format(packet.addr3))
    #                 # if not toDS and fromDS:
    #                 #     print("*** From DS to STA via AP ***")
    #                 #     print("Receiver Address: {0}".format(packet.addr1))
    #                 #     print("Transmitter Address: {0}".format(packet.addr2))
    #                 #     print("Destination Address: {0}".format(packet.addr3))

                
    #             else:
    #                 pass
    #         except Exception as e:
    #             print(e)

    #         count += 1

    #     return access_data

    def pcap_reader(self, filename, output_file):
        #　ファイルが存在しない場合
        if not os.path.isfile(filename):
            print("{0} does not exits".format(filename))
            sys.exit(-1)
        else:
            print("successed read: {0}".format(filename))
        
        count = 0

        # MACアドレスをキーとした辞書を作成する
        access_data = {}

        # MACアドレスのリストを取得
        column_name = "mac_addr"
        table_name = "user"
        addr_list = self.get_addr_list(column_name, table_name)

        # with PcapReader(filename) as packets:
        #     # 1パケットずつ処理する
        #     for packet in packets:
        for packet in PcapReader(filename):
            try:
                # 802.11レイヤーのパケットのみを処理
                if packet.haslayer(Dot11) and packet.type==2: # タイプ2 = Data Frames
                    # print("packet No.{0}".format(count))
                    # flagの特定部分を抽出
                    DS_flag = packet.FCfield & 0x3
                    # DS(Distribution System)に向かうかどうかを判定
                    toDS = DS_flag & 0x01 != 0
                    fromDS = DS_flag & 0x2 != 0

                    if toDS and not fromDS:
                        # MACアドレスが登録されているかどうか
                        if packet.addr2 in addr_list:
                            # 送信者(=スマホ)のMACアドレスを格納
                            TA = packet.addr2
                            # パケットの到着時間を取得
                            packet_time = dt.datetime.fromtimestamp(packet.time, dt.timezone(dt.timedelta(hours=9)))

                            # print(TA, packet_time)
                            access_data[TA] = packet_time                    
                else:
                    pass
            except Exception as e:
                print(e)

            count += 1

        return access_data


    def get_addr_list(self, column_name, table_name):
        addr_list = self.db.select(column_name, table_name)
        return addr_list



if __name__ == "__main__":
    wp = wlan_pcap()

    column_name = "mac_addr"
    table_name = "user"
    wp.get_addr_list(column_name, table_name)
