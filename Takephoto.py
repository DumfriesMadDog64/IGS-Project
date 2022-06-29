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
        #cv2.imshow("images",np.hstack([output]))
        #cv2.waitKey(0)

    #The opened photo stays open until the user presses a button on their keyborad
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
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.waitKey(0)

    #convertDataToCoords(xCoords, yCoords)
    convertDataToCoords(xCoords,yCoords)

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
        if y >= 0 and y <= 175:
            ySorted.append(150)
        elif y > 175 and y <= 275:
            ySorted.append(230)
        elif y > 275 and y <= 350:
            ySorted.append(310)
        elif y > 350 and y <= 450:
            ySorted.append(400)
        elif y > 450 and y <= 525:
            ySorted.append(480)
        elif y > 525  and y <= 600:
            ySorted.append(575)
        elif y > 600 and y <= 700:
            ySorted.append(650)
        elif y > 700 and y <= 775:
            ySorted.append(732.5)
        elif y > 775 and y <= 860:
            ySorted.append(830)
        elif y > 860 and y <= 950:
            ySorted.append(900)
        elif y > 950 and y <= 1050:
            ySorted.append(1000)
        elif y > 1050 and y <= 1150:
            ySorted.append(1090)
        elif y > 1150 and y <= 1200:
            ySorted.append(1175)
        elif y > 1200 and y <= 1300:
            ySorted.append(1270)
        elif y > 1300 and y <= 1400:
            ySorted.append(1350)
        elif y > 1400 and y <= 1500:
            ySorted.append(1450)
        elif y > 1500 and y <= 1600:
            ySorted.append(1550)
        elif y > 1600 and y <= 1700:
            ySorted.append(1640)
        elif y > 1700 and y <= 1750:
            ySorted.append(1725)
        else:
            ySorted.append(1800)

 
    for x in xCoords:
        if x >= 0 and x <= 150:
            xSorted.append(130)
        elif x > 150 and x <= 250:
            xSorted.append(230)
        elif x > 250 and x <= 350:
            xSorted.append(330)
        elif x > 350 and x <= 450:
            xSorted.append(430)
        elif x > 450 and x <= 550:
            xSorted.append(530)
        elif x > 550 and x <= 650:
            xSorted.append(630)
        elif x > 650 and x <= 750:
            xSorted.append(730)
        else: 
            xSorted.append(830)   
    gridCreater(xSorted, ySorted)


takephoto([40,40,40],[70,255,255])
