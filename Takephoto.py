import cv2
from datetime import datetime

from numpy import save

def takephoto():
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
<<<<<<< HEAD
    camera = cv2.VideoCapture(0)
    for i in range(1):
        return_value, image = camera.read()
        cv2.imwrite('opencv'+str(date)+'.png', image)
=======
    camera = cv2.videocapture(0)
    return_value, image = camera.read()
    cv2.imwrite('opencv'+str(date)+'.png', image)
>>>>>>> 588134a319c6b19b095e40dcf42ae73571f4b50f
    del(camera)
    print("done")
    save

takephoto