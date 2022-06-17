import cv2
from datetime import datetime

from numpy import uint8

def takephoto():
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite('opencv'+str(date)+'.png', image)
    img = camera
    del(camera)
    print("Photo Done")
    return img
takephoto() 

