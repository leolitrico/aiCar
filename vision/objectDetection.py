import imageClassificaiton
from picamera2 import Picamera2
import cv2
import time
import rotation


def processCoordinates(ymin, xmin, ymax, xmax, imH, imW):
    centerX = imW - (xmax - xmin) / 2
    areaRatio = ((ymax - ymin) * (xmax - xmin)) / (imH * imW)
    return (deltaX, areaRatio)


def producer(threadQueue):
    # setup camera
    picam = Picamera2()
    picam.start()
    time.sleep(2)

    # get first reference image
    initialImage = picam.capture_array()
    ref = imageProcessing(initialImage).astype("float")

    imageWidth = len(initialImage[1])

    # counter to limit data production amount, and get good averages for right or left or front or back
    previousAreaRatio = 0

    while(1):
        # get a frame as an array of RGB
        image = picam.capture_array()

        # process our image
        image = rotation.rotate_image(image, 180)

        result = imageClassificaiton.findPersonCoordinates(image)
        previousAreaRatio
        if result != None:
            (deltaX, areaRatio) = processCoordinates(result._1,
                                                     result._2, result._3, result._4, result._5, result._6)
            deltaArea = previousAreaRatio - areaRatio
            threadQueue.push((deltaX, deltaArea))
