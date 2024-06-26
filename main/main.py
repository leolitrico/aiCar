#main program, make car follow an object (defined in vision/imageClassification)
from queue import Queue
from threading import Thread
import sys

sys.path.insert(0, '/home/pi/aiCar/carControl')
sys.path.insert(0, '/home/pi/aiCar/vision')
sys.path.insert(0, '/home/pi/aiCar/network')
import objectDetection
import carSetup
import carThread
import imageClassification
import server

serverOn = True

#setup, or stop locomotion if keyboard interrupt received
try:
    threadQueue = Queue() #initialise thread queue
    carSetup.setup() #setup car control

    sock = None
    if serverOn:
        sock = server.setupServer() #setup server

    #initialise carControl thread, and object detection thread and start them 
    t1 = Thread(target=carThread.consumer, args=(threadQueue, ))
    t2 = Thread(target=objectDetection.producer, args=(threadQueue, imageClassification.getInterpreter(), sock, ))
    t1.start()
    t2.start()

except KeyboardInterrupt:
    print("program terminated")
    carSetup.end()
    sys.exit()
