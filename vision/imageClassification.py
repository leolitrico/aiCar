import os
import argparse
import cv2
import numpy as np
import sys
import glob
import importlib.util
from tflite_runtime.interpreter import Interpreter

sys.path.insert(0, '/home/pi/aiCar/network')
import server

# minimum score needed to get a correct classification of our object
minScoreThreshold = 0.45

#object we want to detect
object = "person"

#method to get the score and index of the object with the max score
def getMaxScore(list):
    maxScore = 0
    index = 0
    for score, i in list:
        if score > maxScore:
            maxScore = score
            index = i
    return maxScore, index

def getInterpreter():
     # Path to the model's graph which will detect our objects
    graphPath = "/home/pi/aiCar/tfliteModel/detect.tflite"

    # Path to labelmap
    labelPath = "/home/pi/aiCar/tfliteModel/labelmap.txt"

    # Load the label map
    with open(labelPath, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    interpreter = Interpreter(model_path=graphPath)

    interpreter.allocate_tensors()

    # Get model input and output details
    inputDetails = interpreter.get_input_details()
    outputDetails = interpreter.get_output_details()
    height = inputDetails[0]['shape'][1]
    width = inputDetails[0]['shape'][2]

    outname = outputDetails[0]['name']

    if ('StatefulPartitionedCall' in outname):
        boxesIndex, classesIndex, scoresIndex = 1, 3, 0
    else:
        boxesIndex, classesIndex, scoresIndex = 0, 1, 2

    return (interpreter, height, width, inputDetails, outputDetails, boxesIndex, classesIndex, scoresIndex, labels)

def findPersonCoordinates(image, interpreterDetails, sock):

    (interpreter, height, width, inputDetails, outputDetails, boxesIndex, classesIndex, scoresIndex, labels) = interpreterDetails
    # resize the image to the input specifications made by ml model
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    imageResized = cv2.resize(imageRGB, (width, height))
    inputData = np.expand_dims(imageResized, axis=0)

    # run the model on our image
    interpreter.set_tensor(inputDetails[0]['index'], inputData)
    interpreter.invoke()

    # get the detection results
    boxes = interpreter.get_tensor(outputDetails[boxesIndex]['index'])[
        0]
    classes = interpreter.get_tensor(outputDetails[classesIndex]['index'])[
        0]
    scores = interpreter.get_tensor(outputDetails[scoresIndex]['index'])[
        0]

    #get the objects that could qualify as a sports ball
    potentialObjects = []
    for i in range(0, len(scores)):
        label = labels[int(classes[i])]
        if label == object:
            potentialObjects.append((scores[i], i))

    #if we have potential candidates, find the one with max score, and if it is above our minimum score threshold, then output
    lengthArray = len(potentialObjects)
    if lengthArray > 0:
        score, index = getMaxScore(potentialObjects)
        
        if(score > minScoreThreshold):
            ymin = int(max(1, (boxes[index][0] * imH)))
            xmin = int(max(1, (boxes[index][1] * imW)))
            ymax = int(min(imH, (boxes[index][2] * imH)))
            xmax = int(min(imW, (boxes[index][3] * imW)))

            cv2.putText(image, object, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
            if sock != None:
                server.sendImage(image, sock)

            return (ymin, xmin, ymax, xmax, imH, imW)

    if sock != None:
        server.sendImage(image, sock)
    
    return None
