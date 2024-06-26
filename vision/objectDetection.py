import imageClassification
from picamera2 import Picamera2
import cv2
import time
import rotation

#process the coordinates of our detected object to get it center
def processCoordinates(ymin, xmin, ymax, xmax, imH, imW):
    centerX = (xmax - xmin) / 2 + xmin
    centerY = (ymax - ymin) / 2 + ymin
    deltaX = centerX - imW / 2
    deltaY = centerY - imH / 2
    return (deltaX, deltaY)

#main function used to find objects in each frame, and send its coordinates to the car thread using a queue
def producer(threadQueue, interpreterDetails, sock):
    # setup camera
    picam = Picamera2()
    picam.start()
    time.sleep(2)

    #counter = 0 #counter for delay between objectDetection and carControl

    frameCounterLimit = 1
    frameCounter = 0
    totalDeltaX = 0
    totalDeltaY = 0

    while(1):
        # get a frame as an array of RGB
        image = picam.capture_array()

        # process our image
        image = rotation.rotate_image(image, 180)

        result = imageClassification.findPersonCoordinates(image, interpreterDetails, sock)
        if result != None:
            (deltaX, deltaY) = processCoordinates(result[0],
                                                  result[1], result[2], result[3], result[4], result[5])
            frameCounter += 1
            totalDeltaX += deltaX
            totalDeltaY += deltaY

            #only send data to the threadQueue if we have received {sendDataCounterLimit} amounts of frames that had objects in them
            if frameCounter == frameCounterLimit:
                #send the average position of the object detected in the different frames 
                threadQueue.put((totalDeltaX / frameCounter, totalDeltaY / frameCounter))
                #print("Object detection: " + str(counter))
                #counter += 1

                #reset variables
                frameCounter = 0
                totalDeltaX = 0
                totalDeltaY = 0
