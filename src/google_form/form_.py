# -*- coding: utf-8 -*-
# 引数（名前, 入退室日時）

# requestsのインストールが必要
import requests
import json
import sys

def form(name, time):
    if name == 'tamakawa':
        fname = "tamakawa_cfg.json"
    elif name == 'komiya':
        fname = "komiya_cfg.json"
    else:
        print('該当者なし')
        sys.exit(1)

    # 回答フォームの作成
    with open(fname, "r") as f:
        cfg = json.load(f)
        cfg['output']['time'] = time

        params = {"entry.{}".format(cfg["entry"][k]): cfg["output"][k] for k in cfg["entry"].keys()}
        res = requests.get(cfg["form_url"] + "formResponse", params=params)

    # 回答ができてるかの確認
    if res.status_code == 200:
        print("Done!")
    else:
        res.raise_for_status()
        print("Error")