import sys
sys.path.append('../')

import cv2
import numpy as np
import os 
import pandas as pd
import requests
import time
from line import line_func
from db_src import db_func
from access import access_manage
from access import audio_output
from kafka_src import kafka_func
import datetime
from datetime import datetime as dt


class face_rec:

    def __init__(self):

        # データベースへの接続
        self.db = db_func.db_func()

        # LINE機能を使うためのインスタンス
        self.line = line_func.line_func()

        # 入退室情報を管理機能
        self.access = access_manage.access()

        # ユーザ名を叫ぶためのやつ
        self.ao = audio_output.audio_output()

        # kafka用
        topic_name = "test"
        self.kafka = kafka_func.kafka_func(topic_name, True)
       

    def get_user_list(self):
        # データベースから学習画像があるユーザ一覧を取得する
        field_name = "*"
        table_name = "user"
        wh_field = "img_num"
        value = 0

        user_list = self.db.get_where(field_name, table_name, wh_field ,value, True)
        # user_list = self.db.get_where(field_name, table_name, wh_field ,value)

        self.user_info = []

        for value in user_list:
            user_dic = {
                    "id" : value[0],
                    "student_id" : value[1],
                    "user_name" : value[2],
                    "full_name" : value[3],
                    "token" : value[4]
            }

            self.user_info.append(user_dic)


        return self.user_info
    

    def recognition(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadePath = "Cascades/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        cam.set(3, 640) # set video widht
        cam.set(4, 480) # set video height

        # # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)


        match_count = 0
        prev_user_name = ""

        while True:

            ret, img =cam.read()

            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
            )
            
            for(x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):
                    # id = names[id]
                    for value in self.user_info:
                        if value["id"] == id:
                            match_user = value
                            user_name = value["user_name"]
                            break

                    # user_name = self.user_dic["user_info"]["user_name"]
                    confidence_str = "  {0}%".format(round(100 - confidence))
                else:
                    user_name = "unknown"
                    confidence_str = "  {0}%".format(round(100 - confidence))
                    match_count = 0
                
                if prev_user_name == user_name and not user_name=="unknown"  and (100-confidence) >= 15:
                    match_count = match_count + 1
                else:
                    match_count = 0

                if match_count >= 3:
                    # self.line.line_push(match_user, "")
                    access_flag = self.access.access_manage(match_user)
                    self.kafka.send_json(match_user)
                    # self.line.detect_push(match_user, access_flag)
                    self.ao.user_scream(user_name)
                    match_count = 0

                prev_user_name = user_name
                
                cv2.putText(img, user_name, (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence_str), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            
            cv2.imshow('camera',img) 

            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
            if k == 27:
                break

        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()


    def main(self):
        # self.access.exit_manage()
        face_rec.get_user_list()
        face_rec.recognition()
        
if __name__ == "__main__":
    face_rec = face_rec()
    face_rec.main()

    # user_info = face_rec.get_user_list()
    

    # face_rec.access_manage(user_info[0])

