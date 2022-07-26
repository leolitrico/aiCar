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

#x coordinate of shape, width of shape, width of image)
def deltaX(x, w, imageWidth):
    center = x + w/2
    delta = center - imageWidth/2
    return delta

def producer(threadQueue):
    #setup camera
    picam = Picamera2()
    picam.start()
    time.sleep(2)

    #get first reference image
    initialImage = picam.capture_array()
    ref = imageProcessing(initialImage).astype("float")

    imageWidth = len(initialImage[1])

    #counter to limit data production amount, and get good averages for right or left or front or back
    totalX = 0
    totalArea = 0
    counter = 0




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

        x = 0
        area = 0
        counter += 1
        cv2.imshow("Thresh", imageDiff)

        if len(contours) > 0:
            shapes = [cv2.contourArea(c) for c in contours]

            max_index = np.argmax(shapes)
            maxContour = contours[max_index]   
            for R in shapes:

                # draw a rectangle around the largest contour
                x,y,w,h = cv2.boundingRect(R)
                #for showing the rectangle on the processed image
                cv2.rectangle(grayImage, (x,y), (x+w,y+h), (0,255,0), 2)
            area = cv2.contourArea(maxContour)
        
        totalX += x
        totalArea += area

        if(counter == 0):
            deltaX = totalX / counterLimit
            deltaArea = (totalArea1 - totalArea2) / counterlimit
            data = (deltaX, )
            threadQueue.push(data)
            counter = counterLimit

        counter-=1

        # show the frame
        cv2.imshow("Result", grayImage)   

        # if the 'q' key is pressed then break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
    cv2.destroyAllWindows()



    

