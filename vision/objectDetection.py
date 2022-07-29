import imageClassificaiton
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


def producer(threadQueue):
    # setup camera
    picam = Picamera2()
    picam.start()
    time.sleep(2)

    while(1):
        # get a frame as an array of RGB
        image = picam.capture_array()

        # process our image
        image = rotation.rotate_image(image, 180)

        result = imageClassificaiton.findPersonCoordinates(image)
        if result != None:
            (deltaX, deltaY) = processCoordinates(result._1,
                                                  result._2, result._3, result._4, result._5, result._6)
            threadQueue.push((deltaX, deltaY))
