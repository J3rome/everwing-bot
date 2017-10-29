import os
import argparse
import cv2
from time import sleep

# Helpers modules
import adbWrapper as adb
import imgProcessor


def startAd():
    buttonScreenImgPath = os.path.join(os.getcwd(), 'capture/buttonScreen.png')

    adb.takeScreenCapture(buttonScreenImgPath)
    tapPosition = imgProcessor.getTapPositionFromButtonScreen(buttonScreenImgPath)
    adb.sendTap(tapPosition[0], tapPosition[1])
    print(">> Ad started")


def waitForAdToFinish():
    sleepTime = 5  # 5 seconds

    progressScreenImgPath = os.path.join(os.getcwd(), 'capture/progressScreen.png')

    inProgress = True

    while inProgress:
        adb.takeScreenCapture(progressScreenImgPath)
        if imgProcessor.isEndScreen(progressScreenImgPath):
            inProgress = False
        else:
            print(">>> Waiting for ad to finish...")
            sleep(sleepTime)

    print(">> Ad is Finished !")

    return progressScreenImgPath

def findAdLength():
    # Ad must be started for this to work
    progressScreenImgPath = os.path.join(os.getcwd(), 'capture/progressScreen.png')

    firstTimeStamp = adb.takeScreenCapture(progressScreenImgPath)
    firstProgress = imgProcessor.getAdProgress(progressScreenImgPath)*100

    # TODO : Verify if work with less time
    sleep(2)

    secondTimeStamp = adb.takeScreenCapture(progressScreenImgPath)
    secondProgress = imgProcessor.getAdProgress(progressScreenImgPath)*100

    progressDif = secondProgress - firstProgress
    timeDiff = secondTimeStamp - firstTimeStamp

    timeDiffSec = timeDiff.seconds + timeDiff.microseconds/1e6

    print("Time Diff : ")
    print(timeDiff)

    print("Time diff sec : ")
    print(timeDiff.seconds + timeDiff.microseconds/1e6)

    print("Progress diff : ")
    print(progressDif)

    print("Progress 1 : ")
    print(firstProgress)

    print("Progress 2 : ")
    print(secondProgress)

    progressPerSec = progressDif/timeDiffSec

    progressToGo = 100 - secondProgress

    timeToGo = progressToGo/progressPerSec

    print(str(timeToGo) + " sec before ad end")

    sleep(timeToGo)

    print("Ad as ended !")





# FIXME : This should be done via image recognition instead of hard coded..
def closeAd(endScreenImgPath):
    img = cv2.imread(endScreenImgPath)
    imgHeight, imgWidth, _ = img.shape

    adb.sendTap(imgWidth * 0.963, imgHeight * 0.053)

    print(">> Ad closed")


def doLvlUp(nb=1):
    """
    Must be on lvl up screen before launching
    :return:
    """
    for i in range(0, nb):
        print("> Lvl " + str(i+1))
        startAd()
        endScreenImgPath = waitForAdToFinish()
        closeAd(endScreenImgPath)
        sleep(0.5)


def main():

    # Parsing arguments
    parser = argparse.ArgumentParser(description="Simple everwing auto ad watcher")

    parser.add_argument('-nb', action='store', dest='nbOfLvl', type=int, default=5)

    options = parser.parse_args()

    print("Be sure to have you android phone connected in debugger mode before running this script !")
    print("You also need to be on the character menu where you can watch a video to get a new level")
    print("This script will attempt to lvlup your character by "+str(options.nbOfLvl)+" lvl")
    input("Press Enter to continue...")

    doLvlUp(options.nbOfLvl)

    print("done")


if __name__ == "__main__":
    main()
