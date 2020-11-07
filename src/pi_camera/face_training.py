import cv2
import numpy as np
from PIL import Image
import os

os.environ['LD_PRELOAD'] = '/usr/lib/arm-linux-gnueabihf/libatomic.so.1'

# Path for face image database
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml");

# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    count = 0

    for imagePath in imagePaths:

        # PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        PIL_img = Image.open(imagePath)
        img_numpy = np.array(PIL_img,'uint8')

        filename_list = os.path.split(imagePath)[-1].split(".")

        user_name = filename_list[0]
        id = int(filename_list[1])
        img_num = int(filename_list[2])
        
        print(id)

        faces = detector.detectMultiScale(img_numpy)
        

        count = count + 1

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])

            cv2.imwrite("train_data/{0}.{1}.{2}.jpg".format(user_name, id, img_num),img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))