import sys
import cv2
import time
import datetime
import csv
import os
import pandas as pd

import db_func


class capture_db():

    # 学習画像に関する情報を格納するリスト
    img_info = []

    # ユーザ情報を格納するリスト
    user_info = []

    # ユーザIDを格納
    # user_id = -1

    # 画像の枚数をカウント
    img_num = -1


    def __init__(self):
        # データベースへの接続
        self.db = db_func.db_func()

        # カメラのインスタンス化
        self.cam = cv2.VideoCapture(0)


    def info_input(self):
        # ユーザの名前とLINEトークンを入力させる
        user_name = input('Enter Your User-Name : ')

        # ユーザ情報・撮影情報に格納
        self.user_info.append(user_name)
        self.img_info.append(user_name)

        

        # 新規ユーザの場合
        if self.db.check_user_name(user_name):

            print("")
            print("君はご新規さんだね？")            
            value = input('Enter y or n: ')

            if value == "y":
                student_id = input('Enter Your StudentID (ハイフン入れたらぶっ飛ばすぞって): ')
                full_name = input('Enter Your Full Name: ')
                token = input('Enter Your Token: ')

                self.user_info.append(student_id)
                self.user_info.append(full_name)
                self.user_info.append(token)
            else:
                print("一昨日きやがれ")  
                sys.exit(0)
            
            return True
        # 既存ユーザの場合
        else:
            print("")
            print("君は既存のユーザだね？")            

            value = input('Enter y or n: ')

            if value == "y":
                field_name = "*"
                table_name = "user"
                wh_field = "name"
            

                user_info = self.db.get_where(field_name, table_name, wh_field, user_name)[0]

                # 先頭のユーザid以外をuser_infoに追加する
                for value in user_info[1:]:
                    if not value == self.user_info[0]:
                        self.user_info.append(value)

                print(self.user_info)

    

                return False

            else:
                sys.exit(0)


    def create_user(self, new_user):
        # ユーザ情報の取得
        user_name = self.user_info[0]
        student_id = self.user_info[1]
        full_name = self.user_info[2]
        token = self.user_info[3]

        # 新規ユーザの場合
        if new_user:
            # ユーザを作成
            self.db.create_user(student_id,user_name,full_name,token)

            # 作成したユーザのidを取得する
            user_id = self.db.get_user_id(user_name)
            self.user_info.append(user_id)

            self.img_info.append(user_id)

            return user_id
        # 既存ユーザの場合
        else:
            # ユーザIDを取得する
            user_id = self.db.get_user_id(user_name)
            self.user_info.append(user_id)

            self.img_info.append(user_id)

            return user_id


    def get_img_num(self, user_id):
        field_name = "img_num"
        table_name = "user"
        wh_field = "id"

        # img_num =self.db.select_where(field_name, table_name, self.user_id)
        img_num = self.db.get_where(field_name, table_name, wh_field ,user_id)[0][0]

        self.img_info.append(img_num)

    def capture(self):

        # 学習画像に必要な情報を取得
        user_name = self.img_info[0]
        user_id = self.img_info[1]
        img_num = self.img_info[2] + 1

        # 撮影前の枚数を保持
        img_num_init = img_num

        # 写真撮影回数
        take_num = 99

        # 撮影回数をupdateするのに必要な情報
        table_name = "user"
        field_name = "img_num"

        print("撮影準備はOKかい？")            

        value = input('Enter y or n: ')

        if value == "y":

            while True:
                ret, img = self.cam.read()

                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

                cascadePath = "/home/pi/RAS_src/Cascades/haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(cascadePath);

                # 顔検出を行う
                faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(100, 100))
                
                # 顔が検出された場合
                if len(faces) == 1:
                    # そのときの画像を保存する
                    cv2.imwrite("images/{0}.{1}.{2}.jpg".format(user_name,user_id, img_num),img)

                    print("{0}枚目の画像を撮影しました".format(img_num))
                    img_num = img_num + 1

                    print()

                    # 設定した撮影回数を超えた場合
                    if img_num == img_num_init + take_num:
                        self.db.update_where(table_name, field_name, img_num, user_id)
                        break

                    cv2.imshow('camera',img)

                    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                    if k == 27:
                        break

            # 表示したウィンドウを閉じる
            cv2.destroyAllWindows()
        else:
            print("ByeBye!!")


    def main(self):
        # ユーザ情報を入力させる
        new_user = cap.info_input()

        # ユーザを作成
        user_id = cap.create_user(new_user)

        # ユーザの画像枚数を取得する
        img_num = cap.get_img_num(user_id)

        # 撮影開始!
        cap.capture()




if __name__ == "__main__":
    cap = capture_db()
    cap.main()