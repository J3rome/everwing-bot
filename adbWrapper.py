import subprocess
import os


# TODO : Function isReady(). Should check if there is one device connected via adb. (ONLY 1)
# TODO : Do some error handling. Verify what is returned in stdout and stderr to see if adb connection is possible
def takeScreenCapture(imgPath):
    cmd = "adb shell screencap -p"

    file = open(imgPath,"w")

    subprocess.run(cmd.split(" "), stdout=file)
    file.close()


def sendTap(xCoord, yCoord):
    cmd = "adb shell input tap " + str(xCoord) + " "+str(yCoord)

    subprocess.run(cmd.split(" "))
