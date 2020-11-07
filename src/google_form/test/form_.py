# -*- coding: utf-8 -*-

from os import name
import requests
import json

def form(name, time):
    fname = "cfg.json"
    with open(fname, "r") as f:
        cfg = json.load(f)
        cfg['output']['name'] = name
        cfg['output']['time'] = time

        params = {"entry.{}".format(cfg["entry"][k]): cfg["output"][k] for k in cfg["entry"].keys()}
        res = requests.get(cfg["form_url"] + "formResponse", params=params)

    if res.status_code == 200:
        print("Done!")
    else:
        res.raise_for_status()
        print("Error")


if __name__ == '__main__':
    form('テスト太郎', '2020/11/16 13-19')

