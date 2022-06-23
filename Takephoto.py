from tkinter.tix import IMAGE
import numpy as np
import cv2
import os
from pathlib import Path
from datetime import datetime

def takephoto(max_array, min_array):
    #This creates the variable date that records the exact date and time that the photo is taken
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")

    #This creates the variable imagePath that says which directory the image is going to be stored in
    imagePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos'

    #This creates the variable camera, the fuction cv2.VideoCapture selects the main webcam, if we replace the 0 with a 1 it will use the second camera or webcam
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    
    #imwrite stores the photo to imagePath with the name 'opencv' + the date and time the photo was taken at
    cv2.imwrite(os.path.join(imagePath, 'opencv' + str(date) + '.png'), image)
    
    #deletes the variable camera
    del(camera)
    colourDetection(max_array, min_array, date,imagePath)

def colourDetection(max_array, min_array, date,imagePath):
    #creates the file path where the required image is stored
    filePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos/' + 'opencv' + str(date) + '.png'
    
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
        cv2.imwrite(os.path.join(imagePath, 'opencvCD'+str(date)+'.png'), output)
    #The opened photo stays open until the user presses a button on their keyborad

    colourChange(date,imagePath)

def colourChange(date,imagePath):
    
    #Search for the correct file and load it as a variable called image
    filePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos/' + 'opencvCD' + str(date) + '.png'
    image = cv2.imread(filePath)

    #Sets the range of colours that will be changed
    minColour = np.array([10,10,10])
    maxColour = np.array([256,249,256])

    #Searches the image for all colour in the range and replaces it with gray (RGB = [128,128,128])
    mask = cv2.inRange(image,minColour,maxColour)
    image[mask>0]=(128,128,128)

    #Stores the image to the drive with the date as the file name and calls the next fuction in the sequence
    cv2.imwrite(os.path.join(imagePath, 'opencvCC'+str(date)+'.png'), image)
    blobDetection(date,imagePath)

def blobDetection(date,imagePath):

    #Finds the image from the colourChange and loads it as a variable
    filePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos/' + 'opencvCC' + str(date) + '.png'
    image = cv2.imread(filePath)

    #Sets the parameters of the SimpleBlobDectection function
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 0

    params.maxThreshold = 100

    params.filterByColor = 0

    params.filterByCircularity = False
    
    params.filterByArea = True
    params.minArea = 50
    params.maxArea = 50000

    params.filterByConvexity = False

    params.filterByInertia = False

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(image)

    im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
    cv2.imwrite(os.path.join(imagePath, 'opencvBD'+str(date)+'.png'), im_with_keypoints)
    cv2.imshow("Keypoints", im_with_keypoints)
    cv2.waitKey(0)
    keypointCoor = cv2.KeyPoint_convert(keypoints)
    print(keypointCoor)
    print(len(keypointCoor))
