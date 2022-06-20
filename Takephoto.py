import numpy as np
import cv2
import os
from pathlib import Path
from datetime import datetime

def takephoto(max_array, min_array):
    #This creates the variable date that records the exact date and time that the photo is taken
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")

    #This creates the variable imagePath that says which directory the image is going to be stored in
    imagePath = r'C:\Users\JonathonCrocker\IGS_Project\Auto_Photo\Photos'

    #This creates the variable camera, the fuction cv2.VideoCapture selects the main webcam, if we replace the 0 with a 1 it will use the second camera or webcam
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    
    #imwrite stores the photo to imagePath with the name 'opencv' + the date and time the photo was taken at
    cv2.imwrite(os.path.join(imagePath, 'opencv'+str(date)+'.png'), image)
    
    #deletes the variable camera
    del(camera)
    colourDetection(max_array, min_array, date)

def colourDetection(max_array, min_array, date):

    #creates the file path where the required image is stored
    filePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos/' + "opencv" + str(date) + '.png'
    
    #Creates a variable, image, which is the picture stored at that file path 
    image = cv2.imread(filePath)

    #sets the upper and lower RGB values that will be searched for in the fuction, they need to be flipped as opencv reads RGB values as BGR 
    boundaries = [
        (np.flip(max_array),np.flip(min_array))
    ]

    for (lower,upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

    #Mask is a variable that is the image where, using the inRange function, has had the colour outside the function replaced with black
        mask = cv2.inRange(image,lower,upper)

    #Creates the output, two images side by side, the original picture plus the processed one
        output = cv2.bitwise_and(image, image, mask = mask)

    #Shows the finished photo using the imshow function
        cv2.imshow("images",np.hstack([image,output]))

    #The opened photo stays open until the user presses a button on their keyborad
        cv2.waitKey(0)


takephoto([10,30,30],[90,140,150])
