from tkinter.tix import IMAGE
import numpy as np
import cv2
import os
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

def takephoto(max_array, min_array):
    #This creates the variable date that records the exact date and time that the photo is taken
    date = str(datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p"))

    #This creates the variable imagePath that says which directory the image is going to be stored in
    imagePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos'

    #This creates the variable camera, the fuction cv2.VideoCapture selects the main webcam, if we replace the 0 with a 1 it will use the second camera or webcam
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    
    #imwrite stores the photo to imagePath with the name 'opencv' + the date and time the photo was taken at
    cv2.imwrite(os.path.join(imagePath, 'opencv' + date + '.png'), image)
    
    #deletes the variable camera
    del(camera)
    colourDetection(max_array, min_array, date,imagePath)

def colourDetection(max_array, min_array,date,imagePath):
    #creates the file path where the required image is stored
    filePath = r'C:\Users\JonathonCrocker\downloads/MicrosoftTeams-image (1).png' 
    #Creates a variable, image, which is the picture stored at that file path 
    image = cv2.imread(filePath)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #sets the upper and lower RGB values that will be searched for in the fuction, they need to be flipped as opencv reads RGB values as BGR 
    boundaries = [
        ((max_array),(min_array))
    ]

    for (lower,upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

    #Mask is a variable that is the image where, using the inRange function, has had the colour outside the function replaced with black
        mask = cv2.inRange(hsv,lower,upper)

    #Creates the output, two images side by side, the original picture plus the processed one
        output = cv2.bitwise_and(image, image, mask = mask)

    #Shows the finished photo using the imshow function
        cv2.imshow("images",np.hstack([output]))

    #The opened photo stays open until the user presses a button on their keyborad
        cv2.waitKey(0)
        cv2.imwrite(os.path.join(imagePath, 'opencvCD'+str(date)+'.png'), output)

    colourChange(date,imagePath)

def colourChange(date,imagePath):
    
    #Search for the correct file and load it as a variable called image
    filePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos/' + 'opencvCD' + date + '.png'
    image = cv2.imread(filePath)

    #Sets the range of colours that will be changed
    minColour = np.array([10,10,10])
    maxColour = np.array([256,249,256])

    #Searches the image for all colour in the range and replaces it with gray (RGB = [128,128,128])
    mask = cv2.inRange(image,minColour,maxColour)
    image[mask>0]=(0,128,0)

    #Stores the image to the drive with the date as the file name and calls the next fuction in the sequence
    cv2.imwrite(os.path.join(imagePath, 'opencvCC'+date+'.png'), image)
    blobDetection(date,imagePath)

def blobDetection(date,imagePath):

    #Finds the image from the colourChange and loads it as a variable
    filePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Photos/' + 'opencvCC' + date + '.png'
    image = cv2.imread(filePath)

    #Sets the parameters of the SimpleBlobDectection function
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 0
    params.maxThreshold = 100
    params.filterByColor = 0
    params.filterByCircularity = False
    params.filterByArea = True
    params.minArea = 50
    params.maxArea = 5000    
    params.filterByConvexity = False
    params.filterByInertia = False

    detector = cv2.SimpleBlobDetector_create(params)
    keyPoints = detector.detect(image)

    loopCounter = 0
    xCoords = []
    yCoords = []
    for i in keyPoints:
         xCoords.append(keyPoints[loopCounter].pt[0])
         yCoords.append(keyPoints[loopCounter].pt[1])
         loopCounter = loopCounter + 1

    print(len(xCoords))

    im_with_keypoints = cv2.drawKeypoints(image, keyPoints, np.array([]), (255,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite(os.path.join(imagePath, 'opencvBD'+date+'.png'), im_with_keypoints)
    cv2.imshow("Keypoints", im_with_keypoints)
    cv2.waitKey(0)

    #convertDataToCoords(xCoords, yCoords)
    gridCreater(xCoords,yCoords)


def gridCreater(xCoords, yCoords):
    X = np.array(xCoords)
    Y = np.array(yCoords)
    # Plotting point using scatter method
    plt.scatter(X,Y)
    plt.gca().invert_yaxis()
    plt.show()

# Need to take all of the first numbers in each entry, and add them to a list, then same for second number in each entry 
def convertDataToCoords(xCoords, yCoords):
    xSorted = []
    ySorted = []
 
    for y in yCoords:
        print(y)
        if y >= 0 and y <= 80:
            ySorted.append(40)
        elif y > 80 and y <= 160:
            ySorted.append(120)
        elif y > 160 and y <= 240:
            ySorted.append(200)
        elif y > 240 and y <= 320:
            ySorted.append(280)
        else: 
            ySorted.append(360)

    for x in xCoords:
        if x >= 0 and x <= 87.5:
            xSorted.append(43.75)
        elif x > 87.5 and y <= 175:
            xSorted.append(131.25)
        elif x > 175 and y <= 262.5:
            xSorted.append(218.75)
        elif x > 262.5 and y <= 350:
            xSorted.append(306.25)
        else: 
            xSorted.append(656.25)
    gridCreater(xSorted, ySorted)


takephoto([40,40,40],[70,255,255])
