import numpy as np
import cv2
import os
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt

def takephoto(max_array, min_array):

    #This creates two variables, the first one 'date' that records the exact date and time when the photo was taken and the second one 'imagePath' that records where the image should be stored to
    date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
    imagePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Raw Photos'

    #The first part of the the Try function is the code to take a photo, the second part is what will happen if there is a problem taking and storing the photo
    try:
        #creates a variable called camera and makes it record what the webcam is displaying
        camera = cv2.VideoCapture(0)

        #Creates a new variable called image and tells it to record what camera has stored in it at that moment
        return_value, image = camera.read()

        #Saves image to imagePath then deletes the variable camera then prints "Photo done"
        #cv2.imwrite(os.path.join(imagePath, 'opencv'+str(date)+'.png'), image)
        del(camera)
        
        #Calls the next function, colourDetection, passing the variables through to that function
        colourDetection(max_array, min_array, date, image)
        print("Photo Done")
    except:
        #If the code fails to take or store the photo then it will print "--Failure to take photo--" to the command line
        print("--Failure to take photo--")
    
def colourDetection(max_array, min_array,date,image):
    #Current filePath only there for testing, later will use image from takePhoto
    filePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Test Germination Tray.png' 
    
    #Sets the upper and lower bondaries for the colour detection 
    boundaries = [
        ((max_array),(min_array))
    ]

    for (lower,upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

    #Error catching portion of function, will try to perform colour detection, if it fails it will print "Failure to perform colour detection"
    try:
        #Changes the colour from the image from RGB to HSV for better colour detection
        #Currently reads a test image from the drive, in future this will be the image passed from takePhoto
        image = cv2.imread(filePath)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        #Creates a mask, by scanning the image for colour that lies outside the range and raplacing it with black, then creates the output by overlaying the mask on the original image
        mask = cv2.inRange(hsv,lower,upper)
        output = cv2.bitwise_and(image, image, mask = mask)

        #Shows the output (only necesary for testing)
        #cv2.imshow("images",np.hstack([image,output]))
        #cv2.waitKey(0)
        
        #Calls the next function passing the variable 'date' and 'image' through
        blobDetection(date,image,output)
        print("Colour detection done")       
    except:
        print("--Failure to perform colour detection--")

def blobDetection(date,image,output):

    #We use simpleBlobDetection from opencv to find the green plants in the photo
    #Creates a new variable,'imagePath' which is where to store the blobDetection photos to for future use
    imagePath = r'C:/Users/JonathonCrocker/IGS_Project/Auto_Photo/Blob Detection Photos'

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

    #Error catching portion of function, it will try to perfrom the blob detection, if it fails, it will print an error to the command line
    try:
        #Uses the parameters from above to create a detector then applies that to the image to find the keypoints, the centre of each of the detected blobs
        detector = cv2.SimpleBlobDetector_create(params)
        keyPoints = detector.detect(output)

        #Creates two lists, xCoords and yCoords, the x and y coordinates of the keypoints
        xCoords = []
        yCoords = []

        #Using a for loop, we add the each list by going through the keypoints, adding the y coordinates to yCoords and the x coordinates to xCoords
        loopCounter = 0
        for i in keyPoints:
            xCoords.append(keyPoints[loopCounter].pt[0])
            yCoords.append(keyPoints[loopCounter].pt[1])
            loopCounter = loopCounter + 1


        #calls the next funciton, convertDataToCoords, passing xCoords and yCoords to it
        #convertDataToCoords(xCoords, yCoords)
        X = list(xCoords)
        Y = list(yCoords)
    
        XYCoords = []
        loopCounter = 0
        for i in xCoords:
            XYCoords.append((X[loopCounter],Y[loopCounter]))
            loopCounter = loopCounter + 1
        XYTotal = fuse(XYCoords,50)
        print(len(XYTotal))
        
        #Creates a new image called im_with_keypoints which is the original image with the keypoints superimposed on top of it and then saves this image to the imagePath
        im_with_keypoints = cv2.drawKeypoints(output, keyPoints, np.array([]), (255,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        finalImage = np.hstack([im_with_keypoints,image])
        cv2.imwrite(os.path.join(imagePath, 'opencvBD' + date + '.png'), finalImage)
        
        #Displays im_with_keypoints in a new window
        cv2.imshow("Keypoints", finalImage)
        cv2.waitKey(0)


        gridCreater(XYTotal)
        print("Blob detection done")
    except:
        #If the blobDetection fails for some reason, the message "--Failure to perform blob detection--" will be printed to the command line
        print("--Failure to perform blob detection--")

def dist2(p1, p2):
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def fuse(points, d):
    ret = []
    d2 = d * d
    n = len(points)
    taken = [False] * n
    for i in range(n):
        if not taken[i]:
            count = 1
            point = [points[i][0], points[i][1]]
            taken[i] = True
            for j in range(i+1, n):
                if dist2(points[i], points[j]) < d2:
                    point[0] += points[j][0]
                    point[1] += points[j][1]
                    count+=1
                    taken[j] = True
            point[0] /= count
            point[1] /= count
            ret.append((point[0], point[1]))
    return ret

def convertDataToCoords(xCoords, yCoords):
    xSorted = []
    ySorted = []
 
 #Not a good method for predicting coords of good plugs, too susceptible to change in the original photo
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
    
    X = list(xSorted)
    Y = list(ySorted)
    
    XYTotal = []
    loopCounter = 0
    for i in xCoords:
        XYTotal.append((X[loopCounter],Y[loopCounter]))
        loopCounter = loopCounter + 1
    XYTotal = list(dict.fromkeys(XYTotal))
    
    print("Number of succesfull plugs =", len(XYTotal))
    print("Imaging Done")

    gridCreater(XYTotal)

def gridCreater(XYTotal):
    # Plotting point using scatter method
    plt.scatter(*zip(*XYTotal))
    plt.gca().invert_yaxis()
    plt.show()
    
takephoto([40,40,40],[70,255,255])
