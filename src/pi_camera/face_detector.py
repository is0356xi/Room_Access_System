import cv2
import numpy as np
from PIL import Image
import os
import pandas as pd

os.environ['LD_PRELOAD'] = '/usr/lib/arm-linux-gnueabihf/libatomic.so.1'

# Path for face image database
path = 'images'

detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml");


# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        filename_list = os.path.split(imagePath)[-1].split(".")

        user_name = filename_list[0]
        id = int(filename_list[1])
        img_num = int(filename_list[2])
    

        faces = detector.detectMultiScale(img_numpy)

        print(user_name)


        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])

            cv2.imwrite("dataset/{0}.{1}.{2}.jpg".format(user_name, id, img_num),img_numpy[y:y+h,x:x+w])
            img_num = img_num + 1
            ids.append(id)

    return faceSamples,ids


faces,ids = getImagesAndLabels(path)