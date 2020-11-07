import sys
import cv2
import time
import datetime
import csv
import os
import pandas as pd


# カメラのインスタンス化
cam = cv2.VideoCapture(0)

# ユーザのID・名前をコマンドライン引数から取得
user_id = int(sys.argv[1])
user_name = sys.argv[2]

# 学習画像に関する情報を格納するリスト
img_info = []

# csvファイルパス
img_csv = "img_info.csv"


# 新規ユーザかどうかのフラグ
new_user = False 

# データフレームのカラム名
columns = ["ID","Name","Img_Num"]
# データフレーム生成関数
def create_df(id, name, num):
  img_info.append(id)
  img_info.append(name)
  img_info.append(num)

  df = pd.DataFrame([img_info], columns=columns)

  return df


# csvファイルがない・初回実行時
if not os.path.exists(img_csv):
  img_num = 1
  df = create_df(user_id, user_name, img_num)
  df.to_csv(img_csv, index=False)

# useridリストを読み込む
df = pd.read_csv(img_csv)
ID_list = list(df.loc[:, "ID"])

# 新規ユーザの場合
if not user_id in ID_list:
  new_user = True
  img_num = 1
  df = create_df(user_id, user_name, img_num)
  # useridリストの更新
  ID_list = list(df.loc[:, "ID"])
# 既存ユーザの場合
else:
  index = ID_list.index(user_id) # useridに対応するのが何行目か取得
  img_num = df.loc[index, "Img_Num"]


# useridに対応するのがdfの何行目かを取得
index = ID_list.index(user_id)


#　写真撮影回数
take_num = 30

# 撮影前の枚数を保持
img_num_init = img_num

while True:
  ret, img =cam.read()

  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  cascadePath = "Cascades/haarcascade_frontalface_default.xml"
  faceCascade = cv2.CascadeClassifier(cascadePath);

  # 顔検出を行う
  faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(100, 100))
  
  # 顔が検出された場合
  if len(faces) == 1:
    # そのときの画像を保存する
    cv2.imwrite("images/{0}.{1}.{2}.jpg".format(user_name,user_id, img_num),img)

    print("{0}枚目の画像を撮影しました".format(img_num))
    img_num = img_num + 1
    if img_num == img_num_init + take_num:
      df.loc[index, "Img_Num"] = img_num
      if new_user:
        df.to_csv(img_csv, mode='a', header=False, index=False)
      else:
        df.to_csv(img_csv, index=False)
      break
  
  cv2.imshow('camera',img)

  k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
  if k == 27:
      break

# 表示したウィンドウを閉じる
cv2.destroyAllWindows()