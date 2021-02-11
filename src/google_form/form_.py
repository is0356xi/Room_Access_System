# -*- coding: utf-8 -*-
# 引数（名前, 入退室日時）

# requestsのインストールが必要
import requests
import json
import sys

# def form(name, time):
#     if name == 'tamakawa':
#         fname = "tamakawa_cfg.json"
#     elif name == 'komiya':
#         fname = "komiya_cfg.json"
#     else:
#         print('該当者なし')
#         sys.exit(1)

#     # 回答フォームの作成
#     with open(fname, "r") as f:
#         cfg = json.load(f)
#         cfg['output']['time'] = time

#         params = {"entry.{}".format(cfg["entry"][k]): cfg["output"][k] for k in cfg["entry"].keys()}
#         res = requests.get(cfg["form_url"] + "formResponse", params=params)

#     # 回答ができてるかの確認
#     if res.status_code == 200:
#         print("Done!")
#     else:
#         res.raise_for_status()
#         print("Error")


class test_func:
    def __init__(self):
        # Googleフォームの事前入室登録
        self.pre_url = "https://docs.google.com/forms/d/e/1FAIpQLSd8ENo4XbvSBQLJlaVNx_0HGtIO3eRrwDAfXjZdoEOyeKVj4Q/viewform?usp=pp_url"
        self.url = "https://docs.google.com/forms/d/e/1FAIpQLSe2DgXoLpk_eTF6tRuUSNpciWYgyl02TWsGlhp-HbrxPkxvrw/viewform?"
        self.entry = {
            "name": 208832475,
            "id": 913668226,
            "time": 1243542068
        }
        self.pre_entry = {
            "name": 2005620554,
            "id": 1045781291,
            "AM": {
                "Sat": 398079830,
                "Sun": 529302472,
                "Mon": 865846575,
                "Tue": 1684882939,
                "Wen": 1757879,
                "Thu": 58381649,
                "Fri": 596693774
            },
            "PM": {
                "Sat": 398079830,
                "Sun": 529302472,
                "Mon": 865846575,
                "Tue": 1684882939,
                "Wen": 1757879,
                "Thu": 58381649,
                "Fri": 596693774
            }
        }


    # Googleフォームの事前入室登録
    def line_push_pre(self):
        # ユーザごとのURLを保持
        url_list = []

        # ユーザ情報の取得
        full_name = 'LINE太郎'
        student_id = '1283712837198'
        token = 'token'
        print(self.url)

        # GoogleフォームのURLを生成
        name = "entry.{0}={1}&".format(self.pre_entry["name"], full_name)
        id = "entry.{0}={1}&".format(self.pre_entry["id"], student_id)
        am = ''
        for k in self.pre_entry["AM"].key():
            am += "entry.{0}={1}&".format(self.pre_entry["AM"][k], "9:00〜12:00")
        pm = ''
        for k in self.pre_entry["PM"].key():
            pm += "entry.{0}={1}&".format(self.pre_entry["PM"][k], "12:00〜22:00")

        url = self.pre_url + name + id + am + pm
        print(url)

if __name__ == "__main__":
    test = test_func()
    test.line_push_pre()