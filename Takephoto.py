import cv2
from datetime import datetime

def takephoto():
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('opencv'+str(date)+'.png', image)
    del(camera)
    print("Photo Taken")
takephoto()