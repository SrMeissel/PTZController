from multiprocessing import Process
import time

def start():
    global process
    process = Process(target=readPosition)

def readPosition():
    CurrentPositionL = ""
    CurrentPositionXL = ""
    while True:
        #change position.txt with robot position file
        position = open("positionL.txt", "r").read().lower()
        if position != CurrentPositionL:
            CurrentPositionL = position
            print("Position Changed!")
        
        position = open("positionXL.txt", "r").read().lower()
        if position != CurrentPositionXL:
            CurrentPositionXL = position
            print("Position Changed!")

        time.sleep(1)
def stop():
    global process
    process.terminate()
