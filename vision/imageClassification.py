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
min_conf_threshold = 0.5

def getInterpreter():
     # Path to the model's graph which will detect our objects
    path_to_graph = "/home/pi/aiCar/tfliteModel/detect.tflite"

    # Path to labelmap
    path_to_labels = "/home/pi/aiCar/tfliteModel/labelmap.txt"

    # Load the label map
    with open(path_to_labels, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del(labels[0])

    interpreter = Interpreter(model_path=path_to_graph)

    interpreter.allocate_tensors()

    # Get model input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    outname = output_details[0]['name']

    if ('StatefulPartitionedCall' in outname):
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:
        boxes_idx, classes_idx, scores_idx = 0, 1, 2

    return (interpreter, height, width, input_details, output_details, boxes_idx, classes_idx, scores_idx, labels)

def findPersonCoordinates(image, interpreterDetails, sock):

    (interpreter, height, width, input_details, output_details, boxes_idx, classes_idx, scores_idx, labels) = interpreterDetails
    # resize the image to the input specifications made by ml model
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # run the model on our image
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # get the detection results
    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[
        0]
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[
        0]
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[
        0]

    #get the objects that could qualify as a sports ball
    potentialSportsBalls = []
    for i in range(0, len(scores)):
        label = labels[int(classes[i])]
        if label == "sports ball":
            potentialSportsBalls.append((scores[i], i))

    #if we have potential candidates, find the one with max probability, and if it is above our minimum score threshold, then output
    if len(potentialSportsBalls) > 0:
        sportsBall = potentialSportsBalls[np.argmax(potentialSportsBalls)]
        
        if(sportsBall._1 > min_conf_threshold):
            index = sportsBall._2
            ymin = int(max(1, (boxes[index][0] * imH)))
            xmin = int(max(1, (boxes[index][1] * imW)))
            ymax = int(min(imH, (boxes[index][2] * imH)))
            xmax = int(min(imW, (boxes[index][3] * imW)))

            cv2.putText(image, label, (xmin, ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
            server.sendImage(image, sock)

            return (ymin, xmin, ymax, xmax, imH, imW)

    server.sendImage(image, sock)
    return None
