from picamera2 import Picamera2
import cv2
import time
import numpy as np
import rotation

#constants 
counterLimit = 30

def imageProcessing(image):
    image = rotation.rotate_image(image, 180)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(grayImage, (21, 21), 0)

def main():
    #setup camera
    picam = Picamera2()
    picam.start()
    time.sleep(2)

    #get first reference image
    initialImage = picam.capture_array()
    ref = imageProcessing(initialImage).astype("float")

    while(1):
        #get a frame as an array of RGB
        image = picam.capture_array()

        #process our image 
        grayImage = imageProcessing(image)

        #find the weighted average between the reference image and the current frame
        cv2.accumulateWeighted(grayImage, ref, 0.05)
        #find the difference between our reference image and the current frame
        imageDiff = cv2.absdiff(grayImage, cv2.convertScaleAbs(ref))

        #convert image to binary and dilate it to have full shapes
        imageDiff = cv2.threshold(imageDiff, 25, 255, cv2.THRESH_BINARY)[1]
        imageDiff = cv2.dilate(imageDiff, None, iterations=2)

        #find the contours of the objects that appear in imageDiff
        contours, _ = cv2.findContours(imageDiff.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow("motion detection", imageDiff)

        if len(contours) > 0:
            shapes = [cv2.contourArea(c) for c in contours]

            maxIndex = np.argmax(shapes)
            maxContour = contours[maxIndex]  

            # draw a rectangle around the largest contour
            x,y,w,h = cv2.boundingRect(maxContour)
            #show the rectangle on the processed image
            cv2.rectangle(grayImage, (x,y), (x+w,y+h), (0,255,0), 2)

        # show the frame
        cv2.imshow("motion detection with frame", grayImage)   

        # if the 'q' key is pressed then break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
    cv2.destroyAllWindows()



    

