import subprocess

def takeScreenCapture(imgPath):
    cmd = "adb shell screencap -p"

    file = open(imgPath,"w")

    subprocess.run(cmd.split(" "), stdout=file)
    file.close()

def sendTap(xCoord, yCoord):
    cmd = "adb shell input tap " + str(xCoord) + " "+str(yCoord)

    subprocess.run(cmd.split(" "))