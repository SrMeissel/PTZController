from multiprocessing import Process, Manager
import time

process = None

def start(nameSpace):
    global process
    process = Process(target=readPosition, args=(nameSpace, ))
    process.start()

def readPosition(nameSpace, robotDir = "c:/Release/ordresweepL.txt.status"):
    CurrentPositionL = ""
    CurrentPositionXL = ""

    CurrentPositionSingle = ""

    positionToPreset = {}
    

    data = open("presets.txt").read().lower().splitlines()
    for i, dataPoint in enumerate(data):
        line = dataPoint.split(":")
        positionToPreset[line[1]] = line[0]

    default_Follow = False

    while True:

        if(default_Follow == True):
            try:
                position = open("c:/Release/ordresweepL.txt.status", "r").read().lower()
            except:
                position = CurrentPositionL

            if position != CurrentPositionL:
                CurrentPositionL = position
                nameSpace.camera1_preset = positionToPreset[position]
                print("L Position Changed: ", position)

            try:
                position = open("c:/Release/ordresweepXL.txt.status", "r").read().lower()
            except:
                position = CurrentPositionXL

            if position != CurrentPositionXL:
                CurrentPositionXL = position
                nameSpace.camera2_preset = positionToPreset[position]
                print("XL Position Changed:", position)


        if(default_Follow == False):
            try:
                position = open(robotDir, "r").read().lower()
            except:
                position = ''
            if position != CurrentPositionL:
                CurrentPositionSingle = position

            if position.split("p")[0] == "c1":
                nameSpace.camera1_preset = positionToPreset[position]
                print("Left Position Changed: ",  positionToPreset[position])
            elif position.split("p")[0] == "c2":
                nameSpace.camera2_preset = positionToPreset[position]
                print("Right Position Changed:", positionToPreset[position])


        time.sleep(1)
def stop():
    global process
    process.terminate()
