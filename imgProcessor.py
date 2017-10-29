import numpy as np
import cv2


def findCenterOfMask(mask):
    # FIXME: mask.copy() ?
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]

    # TODO : Choose the good contour, for now we only process the first contour
    contour = contours[0]

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

    buttonZoneStartY = int(imgHeight * 0.63)
    buttonZoneEndY = int(imgHeight * 0.75)

    # TODO : find the button position on whole screenshot instead of cropping. Have to diferenciate between multiple pink
    imgCropped = img[buttonZoneStartY:buttonZoneEndY]

    # Button Pink RGB : (255, 38, 220)
    buttonColorBoundaries = {
        "lower": np.array([200, 25, 240], dtype='uint8'),
        "upper": np.array([240, 50, 255], dtype='uint8')
    }

    # Create the mask
    buttonMask = cv2.inRange(imgCropped, buttonColorBoundaries['lower'], buttonColorBoundaries['upper'])
    buttonMask = cv2.dilate(buttonMask, np.ones((50, 50), np.uint8))

    # Find the center of the mask
    center = findCenterOfMask(buttonMask)

    return center[0], buttonZoneStartY + center[1]


def isEndScreen(imgPath):
    img = cv2.imread(imgPath)
    imgHeight, imgWidth, imgChannels = img.shape

    cropZoneStartY = int(imgHeight * 0.65)
    cropZoneStopY = int(imgHeight * 0.90)

    imgCropped = img[cropZoneStartY:cropZoneStopY]

    # Average all pixel intensity for all channels in 1 value
    averageColorIntensity = np.average(np.average(np.average(imgCropped, axis=0), axis=0), axis=0)

    # We know that the ad is not finished if the background is black
    return averageColorIntensity > 200

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

    progressBarMask = cv2.inRange(imgCropped, progressBarColorBoundaries['lower'], progressBarColorBoundaries['upper'])

    image, contours, hier = cv2.findContours(progressBarMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # TODO : find the button position on whole screenshot instead of cropping. Have to diferenciate between multiple pink
    contour = contours[0]

    _, _, width, _ = cv2.boundingRect(contour)

    progressPercentage = float(width)/imgWidth

    return progressPercentage

## UNUSED
def getExitTapPosition(imgPath):
    img = cv2.imread(imgPath)
    imgHeight, imgWidth, imgChannels = img.shape

    cropZoneStartY = int(imgHeight * 0.01)
    cropZoneStopY = int(imgHeight * 0.05)

    cropZoneStartX = int(imgWidth * 0.912)
    cropZoneStopX = int(imgWidth * 0.985)

    imgCropped = img[cropZoneStartY:cropZoneStopY, cropZoneStartX:cropZoneStopX]

    cv2.imshow("Progress", imgCropped)
    cv2.waitKey(0)
