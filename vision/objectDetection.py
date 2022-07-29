import imageClassification
from picamera2 import Picamera2
import cv2
import time
import rotation


def processCoordinates(ymin, xmin, ymax, xmax, imH, imW):
    centerX = (xmax - xmin) / 2 + xmin
    centerY = (ymax - ymin) / 2 + ymin
    deltaX = centerX - imW / 2
    deltaY = centerY - imH / 2
    return (deltaX, deltaY)


def producer(threadQueue, interpreterDetails, sock):
    # setup camera
    picam = Picamera2()
    picam.start()
    time.sleep(2)

    while(1):
        # get a frame as an array of RGB
        image = picam.capture_array()

        # process our image
        image = rotation.rotate_image(image, 180)

        result = imageClassification.findPersonCoordinates(image, interpreterDetails, sock)
        if result != None:
            (deltaX, deltaY) = processCoordinates(result[0],
                                                  result[1], result[2], result[3], result[4], result[5])
            threadQueue.push((deltaX, deltaY))
