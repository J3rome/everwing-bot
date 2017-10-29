import numpy as np
import os
import argparse
import cv2
import subprocess
from time import sleep


def findCenterOfMask(mask):
    # FIXME: .copy() ?
    countours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    # We only process the first contour
    contour = countours[0]

    # Calculate the center
    M = cv2.moments(contour)
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])

    return x, y


def getTapPositionFromButtonScreen(imgPath):
    """
    Retrieve the tap position from the button screen shot
    :param imgPath:
    :return: x,y position to tap
    """

    # --- Processing of buttonScreen
    # Crop the image

    img = cv2.imread(imgPath)
    imgHeight, imgWidth, imgChannels = img.shape

    buttonZoneStartY = int(imgHeight*0.63)
    buttonZoneEndY = int(imgHeight*0.75)

    imgCropped = img[buttonZoneStartY:buttonZoneEndY]

    # Button Pink RGB : (255, 38, 220)
    buttonColorBoundaries = {
        "lower": np.array([200, 25, 240],dtype='uint8'),
        "upper": np.array([240, 50, 255],dtype='uint8')
    }

    # Create the mask
    buttonMask = cv2.inRange(imgCropped, buttonColorBoundaries['lower'], buttonColorBoundaries['upper'])
    buttonMask = cv2.dilate(buttonMask, np.ones((50,50), np.uint8))

    # Find the center of the mask
    center = findCenterOfMask(buttonMask)

    return center[0], buttonZoneStartY + center[1]


def oldStuff():
    colorsBoundaries = [
        # B    G   R
        ([0, 105, 254], [0, 107, 255]),     # orange
        ([254, 37, 0], [255, 39, 0]),       # blue
        ([0, 0, 254], [0, 0, 255]),   # red
        ([0, 0, 0], [0, 0, 0])          # Black
    ]

    for (lower, upper) in colorsBoundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        cv2.imshow("Images", np.hstack([image, output]))
        cv2.waitKey(0)
        
def isEndScreen(imgPath):
    img = cv2.imread(imgPath)
    imgHeight, imgWidth, imgChannels = img.shape

    cropZoneStartY = int(imgHeight * 0.65)
    cropZoneStopY = int(imgHeight * 0.90 )

    imgCropped = img[cropZoneStartY:cropZoneStopY]

    # Average all pixel intensity for all channels in 1 value
    averageColorIntensity = np.average(np.average(np.average(imgCropped, axis=0), axis=0), axis=0)

    # We know that the ad is not finished if the background is black
    return averageColorIntensity > 200

def getExitTapPosition(imgPath):
    img = cv2.imread(imgPath)
    imgHeight, imgWidth, imgChannels = img.shape

    cropZoneStartY = int(imgHeight * 0.01)
    cropZoneStopY = int(imgHeight * 0.05)

    cropZoneStartX = int(imgWidth * 0.90)
    cropZoneStopX = int(imgWidth * 0.99)

    imgCropped = img[cropZoneStartY:cropZoneStopY, cropZoneStartX:cropZoneStopX]

    cv2.imshow("Progress", imgCropped)
    cv2.waitKey(0)

def getAdProgress(imgPath):
    img = cv2.imread(imgPath)
    imgHeight, imgWidth, imgChannels = img.shape

    buttonZoneStartY = int(imgHeight * 0.80)
    buttonZoneEndY = int(imgHeight * 0.95)

    imgCropped = img[buttonZoneStartY:buttonZoneEndY]



    # Progress bar RGB : (0, 255, 255)
    progressBarColorBoundaries = {
        "lower": np.array([255, 255, 0], dtype='uint8'),
        "upper": np.array([255, 255, 0], dtype='uint8')
    }

    progressBarMask = cv2.inRange(imgCropped,progressBarColorBoundaries['lower'], progressBarColorBoundaries['upper'])
    cv2.imshow("Progress", progressBarMask)
    cv2.waitKey(0)
    exit()

    # Create the mask
    buttonMask = cv2.inRange(imgCropped, buttonColorBoundaries['lower'], buttonColorBoundaries['upper'])
    buttonMask = cv2.dilate(buttonMask, np.ones((50, 50), np.uint8))

### ADB COMMANDS ###
def takeScreenCapture(imgPath):
    cmd = "adb shell screencap -p"

    file = open(imgPath,"w")

    subprocess.run(cmd.split(" "), stdout=file)
    file.close()

def sendTap(xCoord, yCoord):
    cmd = "adb shell input tap " + str(xCoord) + " "+str(yCoord)

    subprocess.run(cmd.split(" "))

def startAd():
    buttonScreenImgPath = os.path.join(os.getcwd(), 'capture/buttonScreen.png')

    takeScreenCapture(buttonScreenImgPath)
    tapPosition = getTapPositionFromButtonScreen(buttonScreenImgPath)
    sendTap(tapPosition[0], tapPosition[1])

def doLvlUp():
    """
    Must be on lvl up screen before launching
    :return:
    """
    sleepTime = 5   # 5 seconds

    progressScreenImgPath = os.path.join(os.getcwd(), 'capture/progressScreen.png')
    endScreenImgPath = os.path.join(os.getcwd(), 'capture/endScreen.png')

    startAd()

    inProgress = True

    while(inProgress):
        takeScreenCapture(progressScreenImgPath)
        if(isEndScreen(progressScreenImgPath)):
            inProgress = False
        else:
            print("Waiting for ad to finish...")
            sleep(sleepTime)

    print("Ad is Finished ! :D")


doLvlUp()
print("done")

#getAdProgress('images/progressBar_black.png')