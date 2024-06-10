from multiprocessing import Process, Manager
import time

process = None

def start(nameSpace):
    global process
    process = Process(target=readPosition, args=(nameSpace, ))
    process.start()

def readPosition(nameSpace):
    CurrentPositionL = ""
    CurrentPositionXL = ""
    while True:
        position = open("c:/Release/ordresweepL.txt.status", "r").read().lower()
        if position != CurrentPositionL:
            CurrentPositionL = position
            nameSpace.camera1_preset = position
            print("L Position Changed: ", position)
        
        position = open("c:/Release/ordresweepXL.txt.status", "r").read().lower()
        if position != CurrentPositionXL:
            CurrentPositionXL = position
            nameSpace.camera2_preset = position
            print("XL Position Changed:", position)


        time.sleep(1)
def stop():
    global process
    process.terminate()
